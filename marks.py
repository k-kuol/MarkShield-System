from database import get_connection
from audit import log_action
from notifications import create_notification
from config import GRADE_SCALE, MIN_SCORE, MAX_SCORE, MIN_CREDIT_HOURS


def score_to_grade(score):
    for threshold, grade in GRADE_SCALE:
        if score >= threshold:
            return grade
    return "F"


def enter_marks(lecturer_username):
    print("\n--- Enter Student Marks ---")
    student_username = input("Student's username: ").strip()

    with get_connection() as conn:
        student = conn.execute(
            "SELECT * FROM users WHERE username = ? AND role = 'student'", (student_username,)
        ).fetchone()

    if not student:
        print("[!] We couldn't find a student with that username.")
        return

    course_code = input("Course Code: ").strip().upper()
    course_name = input("Course Name: ").strip()

    try:
        credit_hours = int(input("Credit Hours: ").strip())
        score = float(input(f"Score ({MIN_SCORE}-{MAX_SCORE}): ").strip())
    except ValueError:
        print("[!] Please enter valid numbers for credit hours and score.")
        return

    if not (MIN_SCORE <= score <= MAX_SCORE) or credit_hours < MIN_CREDIT_HOURS:
        print(f"[!] Score must be between {MIN_SCORE} and {MAX_SCORE}, and credit hours must be at least {MIN_CREDIT_HOURS}.")
        return

    grade = score_to_grade(score)

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO marks (student_username, course_code, course_name, credit_hours, score, grade, entered_by) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (student_username, course_code, course_name, credit_hours, score, grade, lecturer_username)
        )

    create_notification(student_username, f"A new mark has been recorded for {course_code}: {score} ({grade}).")
    log_action(lecturer_username, "ENTER_MARK", f"Student: {student_username}, Course: {course_code}, Score: {score}")
    print(f"[✓] Mark saved! {course_code} — {score} ({grade})")


def view_student_marks(student_username):
    print(f"\n--- Your Marks ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, course_code, course_name, credit_hours, score, grade, entered_by, entered_at FROM marks WHERE student_username = ? ORDER BY entered_at DESC",
            (student_username,)
        ).fetchall()

    if not rows:
        print("No marks have been recorded for you yet.")
        return

    print(f"{'ID':<5} {'Code':<10} {'Course':<25} {'Credits':<8} {'Score':<8} {'Grade':<6} {'Entered By':<15} {'Date'}")
    print("-" * 95)
    for r in rows:
        print(f"{r['id']:<5} {r['course_code']:<10} {r['course_name']:<25} {r['credit_hours']:<8} {r['score']:<8} {r['grade']:<6} {r['entered_by']:<15} {r['entered_at']}")


def view_submitted_marks(lecturer_username):
    print(f"\n--- Marks You've Submitted ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT m.id, m.student_username, m.course_code, m.score, m.grade, m.entered_at FROM marks m WHERE m.entered_by = ? ORDER BY m.entered_at DESC",
            (lecturer_username,)
        ).fetchall()

    if not rows:
        print("You haven't submitted any marks yet.")
        return

    print(f"{'ID':<5} {'Student':<20} {'Code':<10} {'Score':<8} {'Grade':<6} {'Date'}")
    print("-" * 70)
    for r in rows:
        print(f"{r['id']:<5} {r['student_username']:<20} {r['course_code']:<10} {r['score']:<8} {r['grade']:<6} {r['entered_at']}")


def flag_discrepancy(student_username):
    print("\n--- Flag a Mark Discrepancy ---")
    view_student_marks(student_username)
    try:
        mark_id = int(input("\nEnter the ID of the mark you'd like to flag: ").strip())
    except ValueError:
        print("[!] That doesn't look like a valid ID.")
        return

    with get_connection() as conn:
        mark = conn.execute("SELECT * FROM marks WHERE id = ? AND student_username = ?", (mark_id, student_username)).fetchone()

    if not mark:
        print("[!] We couldn't find that mark, or it doesn't belong to your account.")
        return

    reason = input("What's the reason for flagging this mark? ").strip()
    if not reason:
        print("[!] Please provide a reason before submitting.")
        return

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO flags (student_username, mark_id, reason) VALUES (?, ?, ?)",
            (student_username, mark_id, reason)
        )

    log_action(student_username, "FLAG_DISCREPANCY", f"Mark ID: {mark_id}, Reason: {reason}")
    create_notification(mark["entered_by"], f"{student_username} has flagged mark ID {mark_id} for {mark['course_code']}. Please review.")
    print("[✓] Your flag has been submitted. The relevant lecturer has been notified.")


def track_flags(student_username):
    print(f"\n--- Your Submitted Flags ---")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT f.id, m.course_code, m.score, f.reason, f.status, f.flagged_at, f.resolution_note
               FROM flags f JOIN marks m ON f.mark_id = m.id
               WHERE f.student_username = ? ORDER BY f.flagged_at DESC""",
            (student_username,)
        ).fetchall()

    if not rows:
        print("You haven't submitted any flags yet.")
        return

    for r in rows:
        print(f"\nFlag #{r['id']} | Course: {r['course_code']} | Score: {r['score']} | Status: {r['status'].upper()}")
        print(f"  Your reason: {r['reason']}")
        print(f"  Submitted on: {r['flagged_at']}")
        if r["resolution_note"]:
            print(f"  Admin's response: {r['resolution_note']}")


def request_correction(lecturer_username):
    print("\n--- Request a Mark Correction ---")
    try:
        mark_id = int(input("Enter the ID of the mark to correct: ").strip())
    except ValueError:
        print("[!] That doesn't look like a valid ID.")
        return

    with get_connection() as conn:
        mark = conn.execute("SELECT * FROM marks WHERE id = ? AND entered_by = ?", (mark_id, lecturer_username)).fetchone()

    if not mark:
        print("[!] That mark wasn't found, or you didn't enter it.")
        return

    print(f"Current score: {mark['score']} ({mark['grade']}) for {mark['course_code']}")
    try:
        new_score = float(input(f"What should the correct score be? ({MIN_SCORE}-{MAX_SCORE}): ").strip())
    except ValueError:
        print("[!] Please enter a valid number.")
        return

    if not (MIN_SCORE <= new_score <= MAX_SCORE):
        print(f"[!] Score must be between {MIN_SCORE} and {MAX_SCORE}.")
        return

    reason = input("Why does this mark need to be corrected? ").strip()
    if not reason:
        print("[!] Please provide a reason before submitting.")
        return

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO correction_requests (mark_id, requested_by, old_score, new_score, reason) VALUES (?, ?, ?, ?, ?)",
            (mark_id, lecturer_username, mark["score"], new_score, reason)
        )

    log_action(lecturer_username, "REQUEST_CORRECTION", f"Mark ID: {mark_id}, Old: {mark['score']}, New: {new_score}")
    print("[✓] Your correction request has been sent to the admin for review.")


def view_correction_requests(lecturer_username):
    print(f"\n--- Your Correction Requests ---")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT cr.id, m.course_code, m.student_username, cr.old_score, cr.new_score, cr.reason, cr.status, cr.requested_at
               FROM correction_requests cr JOIN marks m ON cr.mark_id = m.id
               WHERE cr.requested_by = ? ORDER BY cr.requested_at DESC""",
            (lecturer_username,)
        ).fetchall()

    if not rows:
        print("You haven't submitted any correction requests yet.")
        return

    for r in rows:
        print(f"\nRequest #{r['id']} | Course: {r['course_code']} | Student: {r['student_username']} | Status: {r['status'].upper()}")
        print(f"  Score change: {r['old_score']} → {r['new_score']} | Reason: {r['reason']}")
        print(f"  Submitted on: {r['requested_at']}")


def review_corrections(admin_username):
    print("\n--- Pending Mark Correction Requests ---")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT cr.id, m.course_code, m.student_username, cr.requested_by, cr.old_score, cr.new_score, cr.reason, cr.requested_at
               FROM correction_requests cr JOIN marks m ON cr.mark_id = m.id
               WHERE cr.status = 'pending' ORDER BY cr.requested_at""",
        ).fetchall()

    if not rows:
        print("There are no pending correction requests right now.")
        return

    for r in rows:
        print(f"\nRequest #{r['id']} | Course: {r['course_code']} | Student: {r['student_username']} | Lecturer: {r['requested_by']}")
        print(f"  Score change: {r['old_score']} → {r['new_score']} | Reason: {r['reason']}")

    try:
        req_id = int(input("\nEnter the Request ID to review (0 to go back): ").strip())
    except ValueError:
        print("[!] That doesn't look like a valid ID.")
        return

    if req_id == 0:
        return

    with get_connection() as conn:
        req = conn.execute("SELECT * FROM correction_requests WHERE id = ? AND status = 'pending'", (req_id,)).fetchone()

    if not req:
        print("[!] That request wasn't found or has already been reviewed.")
        return

    decision = input("Would you like to approve or reject this request? (a = approve / r = reject): ").strip().lower()
    if decision not in ("a", "r"):
        print("[!] Please enter 'a' to approve or 'r' to reject.")
        return

    status = "approved" if decision == "a" else "rejected"

    with get_connection() as conn:
        conn.execute(
            "UPDATE correction_requests SET status = ?, reviewed_by = ?, reviewed_at = CURRENT_TIMESTAMP WHERE id = ?",
            (status, admin_username, req_id)
        )
        if status == "approved":
            mark = conn.execute("SELECT * FROM marks WHERE id = ?", (req["mark_id"],)).fetchone()
            new_grade = score_to_grade(req["new_score"])
            conn.execute(
                "UPDATE marks SET score = ?, grade = ? WHERE id = ?",
                (req["new_score"], new_grade, req["mark_id"])
            )
            create_notification(mark["student_username"], f"Your mark for {mark['course_code']} has been updated to {req['new_score']} ({new_grade}).")
            create_notification(req["requested_by"], f"Your correction request #{req_id} was approved and the mark has been updated.")
        else:
            create_notification(req["requested_by"], f"Your correction request #{req_id} was reviewed but not approved.")

    log_action(admin_username, f"CORRECTION_{status.upper()}", f"Request ID: {req_id}")
    print(f"[✓] Correction request has been {status}.")


def investigate_flags(admin_username):
    print("\n--- Flagged Discrepancies Awaiting Review ---")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT f.id, f.student_username, m.course_code, m.score, m.grade, f.reason, f.flagged_at
               FROM flags f JOIN marks m ON f.mark_id = m.id
               WHERE f.status = 'pending' ORDER BY f.flagged_at""",
        ).fetchall()

    if not rows:
        print("There are no flagged discrepancies to review right now.")
        return

    for r in rows:
        print(f"\nFlag #{r['id']} | Student: {r['student_username']} | Course: {r['course_code']} | Score: {r['score']} ({r['grade']})")
        print(f"  Student's reason: {r['reason']} | Flagged on: {r['flagged_at']}")

    try:
        flag_id = int(input("\nEnter the Flag ID to resolve (0 to go back): ").strip())
    except ValueError:
        print("[!] That doesn't look like a valid ID.")
        return

    if flag_id == 0:
        return

    with get_connection() as conn:
        flag = conn.execute("SELECT * FROM flags WHERE id = ? AND status = 'pending'", (flag_id,)).fetchone()

    if not flag:
        print("[!] That flag wasn't found or has already been resolved.")
        return

    decision = input("Would you like to resolve or dismiss this flag? (r = resolve / x = dismiss): ").strip().lower()
    if decision not in ("r", "x"):
        print("[!] Please enter 'r' to resolve or 'x' to dismiss.")
        return

    status = "resolved" if decision == "r" else "rejected"
    note = input("Leave a note for the student: ").strip()

    with get_connection() as conn:
        conn.execute(
            "UPDATE flags SET status = ?, resolved_by = ?, resolved_at = CURRENT_TIMESTAMP, resolution_note = ? WHERE id = ?",
            (status, admin_username, note, flag_id)
        )

    create_notification(flag["student_username"], f"Your flag #{flag_id} has been {status}. Admin's note: {note}")
    log_action(admin_username, f"FLAG_{status.upper()}", f"Flag ID: {flag_id}, Note: {note}")
    print(f"[✓] Flag has been marked as {status}.")
