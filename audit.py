from database import get_connection
from config import AUDIT_DISPLAY_LIMIT


def log_action(username, action, details=None):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO audit_trail (performed_by, action, details) VALUES (?, ?, ?)",
            (username, action, details)
        )


def view_audit_trail():
    print("\n--- Full System Audit Trail ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT performed_by, action, details, performed_at FROM audit_trail ORDER BY performed_at DESC LIMIT ?",
            (AUDIT_DISPLAY_LIMIT,)
        ).fetchall()

    if not rows:
        print("No activity has been recorded yet.")
        return

    print(f"{'User':<20} {'Action':<25} {'Details':<40} {'Timestamp'}")
    print("-" * 100)
    for r in rows:
        print(f"{r['performed_by']:<20} {r['action']:<25} {str(r['details'] or ''):<40} {r['performed_at']}")


def view_student_mark_history(student_username):
    print(f"\n--- Your Mark Activity History ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT performed_by, action, details, performed_at FROM audit_trail WHERE details LIKE ? ORDER BY performed_at DESC",
            (f"%{student_username}%",)
        ).fetchall()

    if not rows:
        print("No mark activity has been recorded for your account yet.")
        return

    print(f"{'Action':<25} {'Details':<50} {'Timestamp'}")
    print("-" * 90)
    for r in rows:
        print(f"{r['action']:<25} {str(r['details'] or ''):<50} {r['performed_at']}")
