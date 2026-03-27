from database import get_connection


def create_notification(username, message):
    with get_connection() as conn:
        conn.execute(
            "INSERT INTO notifications (username, message) VALUES (?, ?)",
            (username, message)
        )


def view_notifications(username):
    print("\n--- Your Notifications ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, message, is_read, created_at FROM notifications WHERE username = ? ORDER BY created_at DESC",
            (username,)
        ).fetchall()

        if not rows:
            print("You're all caught up — no notifications here.")
            return

        for r in rows:
            status = "     " if r["is_read"] else "[NEW] "
            print(f"{status}{r['created_at']}  {r['message']}")

        conn.execute("UPDATE notifications SET is_read = 1 WHERE username = ?", (username,))


def unread_count(username):
    with get_connection() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM notifications WHERE username = ? AND is_read = 0",
            (username,)
        ).fetchone()
    return result[0]
