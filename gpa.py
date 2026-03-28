from database import get_connection
from config import GRADE_POINTS, GPA_STANDINGS


def calculate_gpa(student_username):
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT course_code, course_name, credit_hours, score, grade FROM marks WHERE student_username = ?",
            (student_username,)
        ).fetchall()

    if not rows:
        return None, []

    total_points = sum(GRADE_POINTS.get(r["grade"], 0) * r["credit_hours"] for r in rows)
    total_credits = sum(r["credit_hours"] for r in rows)
    gpa = total_points / total_credits if total_credits > 0 else 0.0
    return round(gpa, 2), rows


def get_standing(gpa):
    for threshold, label in GPA_STANDINGS:
        if gpa >= threshold:
            return label
    return "At Risk"


def view_gpa_summary(student_username):
    print(f"\n--- Your GPA & Academic Summary ---")
    gpa, rows = calculate_gpa(student_username)

    if gpa is None:
        print("No marks have been recorded yet, so your GPA can't be calculated.")
        return

    print(f"\n{'Course Code':<12} {'Course Name':<25} {'Credits':<8} {'Score':<8} {'Grade':<6} {'Points'}")
    print("-" * 75)
    for r in rows:
        pts = GRADE_POINTS.get(r["grade"], 0)
        print(f"{r['course_code']:<12} {r['course_name']:<25} {r['credit_hours']:<8} {r['score']:<8} {r['grade']:<6} {pts}")

    total_credits = sum(r["credit_hours"] for r in rows)
    max_gpa = max(GRADE_POINTS.values())
    print("-" * 75)
    print(f"\nTotal Credits Earned : {total_credits}")
    print(f"Cumulative GPA       : {gpa:.2f} / {max_gpa:.2f}")
    print(f"Academic Standing    : {get_standing(gpa)}")
