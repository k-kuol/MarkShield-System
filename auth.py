import hashlib
import getpass
from database import get_connection
from audit import log_action
from notifications import create_notification
from config import MIN_PASSWORD_LENGTH


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register():
    print("\n--- Create Your Account ---")
    full_name = input("What's your full name? ").strip()
    username = input("Choose a username: ").strip()
    if not full_name or not username:
        print("[!] Your name and username can't be left blank.")
        return

    print("What is your role?")
    print("  1. Student  2. Lecturer  3. Admin")
    role_map = {"1": "student", "2": "lecturer", "3": "admin"}
    role = role_map.get(input("Pick a number: ").strip())
    if not role:
        print("[!] That's not a valid role. Please choose 1, 2, or 3.")
        return

    password = getpass.getpass("Create a password: ")
    confirm = getpass.getpass("Confirm your password: ")
    if password != confirm:
        print("[!] Those passwords don't match. Please try again.")
        return
    if len(password) < MIN_PASSWORD_LENGTH:
        print(f"[!] Your password needs to be at least {MIN_PASSWORD_LENGTH} characters long.")
        return

    try:
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                (username, hash_password(password), role, full_name)
            )
        create_notification(username, f"Hey {full_name}, welcome to MarkShield! Your account is all set up.")
        log_action(username, "REGISTER", f"New {role} account registered.")
        print(f"[✓] You're all set! You can now log in as a {role}.")
    except Exception:
        print("[!] That username is already taken. Please try a different one.")


def login():
    print("\n--- Log In ---")
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    with get_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE username = ? AND password_hash = ?",
            (username, hash_password(password))
        ).fetchone()

    if user:
        log_action(username, "LOGIN", "User logged in.")
        print(f"\n[✓] Logged in successfully! Good to see you again, {user['full_name']}.")
        return dict(user)
    else:
        print("[!] Hmm, that username or password doesn't look right. Please try again.")
        return None
