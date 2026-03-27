from database import get_connection
from gpa import calculate_gpa, get_standing
from config import GRADE_POINTS


def generate_reports(admin_username):
    while True:
        print("\n--- Generate a Report ---")
        print("1. All Students GPA Summary")
        print("2. Course Performance Overview")
        print("3. Flag & Correction Statistics")
        print("4. Back")
        choice = input("Which report would you like to generate? ").strip()

        if choice == "1":
            _report_all_gpa()
        elif choice == "2":
            _report_course_performance()
        elif choice == "3":
            _report_flag_correction_stats()
        elif choice == "4":
            break
        else:
            print("[!] That's not a valid option. Please choose 1, 2, 3, or 4.")


def _report_all_gpa():
    print("\n=== All Students GPA Summary ===")
    with get_connection() as conn:
        students = conn.execute("SELECT username, full_name FROM users WHERE role = 'student'").fetchall()

    if not students:
        print("No students are registered in the system yet.")
        return

    print(f"{'Username':<20} {'Full Name':<25} {'GPA':<8} {'Standing'}")
    print("-" * 70)
    for s in students:
        gpa, _ = calculate_gpa(s["username"])
        if gpa is None:
            gpa_str, standing = "N/A", "No marks yet"
        else:
            gpa_str = f"{gpa:.2f}"
            standing = get_standing(gpa)
        print(f"{s['username']:<20} {s['full_name']:<25} {gpa_str:<8} {standing}")


def _report_course_performance():
    print("\n=== Course Performance Overview ===")
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT course_code, course_name,
                      COUNT(*) as total_students,
                      AVG(score) as avg_score,
                      MAX(score) as highest,
                      MIN(score) as lowest
               FROM marks GROUP BY course_code ORDER BY course_code"""
        ).fetchall()

    if not rows:
        print("No marks have been entered into the system yet.")
        return

    print(f"{'Code':<10} {'Course':<25} {'Students':<10} {'Avg':<8} {'High':<8} {'Low'}")
    print("-" * 70)
    for r in rows:
        print(f"{r['course_code']:<10} {r['course_name']:<25} {r['total_students']:<10} {r['avg_score']:.1f}{'':4} {r['highest']:<8} {r['lowest']}")


def _report_flag_correction_stats():
    print("\n=== Flag & Correction Statistics ===")
    with get_connection() as conn:
        flag_stats = conn.execute(
            "SELECT status, COUNT(*) as count FROM flags GROUP BY status"
        ).fetchall()
        corr_stats = conn.execute(
            "SELECT status, COUNT(*) as count FROM correction_requests GROUP BY status"
        ).fetchall()

    print("\nDiscrepancy Flags:")
    if not flag_stats:
        print("  No flags have been submitted yet.")
    for r in flag_stats:
        print(f"  {r['status'].capitalize()}: {r['count']}")

    print("\nCorrection Requests:")
    if not corr_stats:
        print("  No correction requests have been submitted yet.")
    for r in corr_stats:
        print(f"  {r['status'].capitalize()}: {r['count']}")