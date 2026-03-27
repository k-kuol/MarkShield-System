from database import initialize_db, seed_demo_data
from auth import register, login
from marks import (
    enter_marks, view_student_marks, view_submitted_marks,
    flag_discrepancy, track_flags, request_correction,
    view_correction_requests, review_corrections, investigate_flags
)
from gpa import view_gpa_summary
from wellness import wellness_checkin, view_wellness_history
from notifications import view_notifications, unread_count
from audit import view_audit_trail, view_student_mark_history
from reports import generate_reports


def show_notification_hint(username):
    count = unread_count(username)
    if count > 0:
        print(f"\n[You have {count} unread notification(s). Head to 'View Notifications' to catch up.]")


def student_menu(user):
    while True:
        show_notification_hint(user["username"])
        print(f"\nHi, {user['full_name']}! What would you like to do?")
        print("1. View My Marks")
        print("2. View My Mark History")
        print("3. Flag a Mark Discrepancy")
        print("4. Track My Flags")
        print("5. View My GPA & Academic Summary")
        print("6. Wellness Check-In")
        print("7. View Notifications")
        print("8. Logout")
        choice = input("Your choice: ").strip()

        if choice == "1":
            view_student_marks(user["username"])
        elif choice == "2":
            view_student_mark_history(user["username"])
        elif choice == "3":
            flag_discrepancy(user["username"])
        elif choice == "4":
            track_flags(user["username"])
        elif choice == "5":
            view_gpa_summary(user["username"])
        elif choice == "6":
            print("\n1. Do a New Check-In\n2. View My Check-In History")
            sub = input("Your choice: ").strip()
            if sub == "1":
                wellness_checkin(user["username"])
            elif sub == "2":
                view_wellness_history(user["username"])
        elif choice == "7":
            view_notifications(user["username"])
        elif choice == "8":
            print(f"See you later, {user['full_name']}!")
            break
        else:
            print("[!] That option doesn't exist. Please pick a number from the menu.")


def lecturer_menu(user):
    while True:
        show_notification_hint(user["username"])
        print(f"\nWelcome back, {user['full_name']}! What would you like to do?")
        print("1. Enter Student Marks")
        print("2. View Marks I've Submitted")
        print("3. Request a Mark Correction")
        print("4. Track My Correction Requests")
        print("5. View Notifications")
        print("6. Logout")
        choice = input("Your choice: ").strip()

        if choice == "1":
            enter_marks(user["username"])
        elif choice == "2":
            view_submitted_marks(user["username"])
        elif choice == "3":
            request_correction(user["username"])
        elif choice == "4":
            view_correction_requests(user["username"])
        elif choice == "5":
            view_notifications(user["username"])
        elif choice == "6":
            print(f"See you later, {user['full_name']}!")
            break
        else:
            print("[!] That option doesn't exist. Please pick a number from the menu.")


def admin_menu(user):
    while True:
        show_notification_hint(user["username"])
        print(f"\nWelcome back, {user['full_name']}! What would you like to do?")
        print("1. Review Pending Mark Corrections")
        print("2. Investigate Flagged Discrepancies")
        print("3. View the Full Audit Trail")
        print("4. Generate Reports")
        print("5. View Notifications")
        print("6. Logout")
        choice = input("Your choice: ").strip()

        if choice == "1":
            review_corrections(user["username"])
        elif choice == "2":
            investigate_flags(user["username"])
        elif choice == "3":
            view_audit_trail()
        elif choice == "4":
            generate_reports(user["username"])
        elif choice == "5":
            view_notifications(user["username"])
        elif choice == "6":
            print(f"See you later, {user['full_name']}!")
            break
        else:
            print("[!] That option doesn't exist. Please pick a number from the menu.")


def main():
    initialize_db()
    seed_demo_data()
    print("\nWelcome to MarkShield — your trusted Student Marks Protection System.")

    while True:
        print("\nWhat would you like to do?")
        print("1. Create an Account")
        print("2. Log In")
        print("3. Exit")
        choice = input("Your choice: ").strip()

        if choice == "1":
            register()
        elif choice == "2":
            user = login()
            if user:
                role = user["role"]
                if role == "student":
                    student_menu(user)
                elif role == "lecturer":
                    lecturer_menu(user)
                elif role == "admin":
                    admin_menu(user)
        elif choice == "3":
            print("Thanks for using MarkShield. Take care!")
            break
        else:
            print("[!] That's not a valid option. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()