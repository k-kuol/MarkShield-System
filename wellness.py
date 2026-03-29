from database import get_connection
from audit import log_action
from config import (
    WELLNESS_MIN, WELLNESS_MAX,
    WELLNESS_HIGH_STRESS_THRESHOLD, WELLNESS_LOW_MOOD_THRESHOLD,
    WELLNESS_HISTORY_LIMIT
)


def wellness_checkin(student_username):
    print("\n--- Wellness Check-In ---")
    print(f"Take a moment to check in with yourself. Rate how you're feeling on a scale of {WELLNESS_MIN} (low) to {WELLNESS_MAX} (high).")

    try:
        mood = int(input(f"How's your mood today? ({WELLNESS_MIN}-{WELLNESS_MAX}): ").strip())
        stress = int(input(f"How stressed are you feeling? ({WELLNESS_MIN}-{WELLNESS_MAX}): ").strip())
    except ValueError:
        print("[!] Please enter whole numbers only.")
        return

    if not (WELLNESS_MIN <= mood <= WELLNESS_MAX) or not (WELLNESS_MIN <= stress <= WELLNESS_MAX):
        print(f"[!] Both values need to be between {WELLNESS_MIN} and {WELLNESS_MAX}.")
        return

    notes = input("Anything else you'd like to note? (Press Enter to skip): ").strip()

    with get_connection() as conn:
        conn.execute(
            "INSERT INTO wellness_checkins (student_username, mood_score, stress_level, notes) VALUES (?, ?, ?, ?)",
            (student_username, mood, stress, notes or None)
        )

    log_action(student_username, "WELLNESS_CHECKIN", f"Mood: {mood}, Stress: {stress}")
    print("[✓] Check-in recorded. Thank you for taking care of yourself!")

    if stress >= WELLNESS_HIGH_STRESS_THRESHOLD:
        print("\n[!] It sounds like you're under a lot of stress. Please consider reaching out to a counselor or someone you trust.")
    elif mood <= WELLNESS_LOW_MOOD_THRESHOLD:
        print("\n[!] It seems like you're having a tough time. Remember, support is always available — you don't have to go through it alone.")


def view_wellness_history(student_username):
    print(f"\n--- Your Wellness Check-In History ---")
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT mood_score, stress_level, notes, checked_in_at FROM wellness_checkins WHERE student_username = ? ORDER BY checked_in_at DESC LIMIT ?",
            (student_username, WELLNESS_HISTORY_LIMIT)
        ).fetchall()

    if not rows:
        print("You haven't done any wellness check-ins yet.")
        return

    print(f"{'Date':<25} {'Mood':<6} {'Stress':<8} Notes")
    print("-" * 70)
    for r in rows:
        print(f"{r['checked_in_at']:<25} {r['mood_score']:<6} {r['stress_level']:<8} {r['notes'] or ''}")
