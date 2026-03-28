# MarkShield — Student Marks Protection System

> *Because every mark matters, and every student deserves transparency.*

MarkShield is a command-line Python application built to bring trust, accountability, and fairness to academic marks management. No more lost corrections, unexplained grade changes, or unanswered disputes — MarkShield keeps everyone in the loop, every step of the way.

---

## What Makes MarkShield Different?

Most mark systems just store numbers. MarkShield goes further:

- **Full audit trail** — every mark entry, change, and correction is logged with a timestamp and the name of who did it
- **Student-powered flagging** — students can raise discrepancy flags directly, no need to chase down lecturers
- **Correction workflow** — lecturers request corrections, admins review them, students get notified
- **Built-in notifications** — no one is left wondering what happened to their request
- **Wellness check-ins** — because academic pressure is real, and we care about more than just grades

---

## Getting Started

**All you need is Python 3.7+** — no pip installs, no virtual environments, no fuss.

```bash
# 1. Clone the repo
git clone https://github.com/k-kuol/MarkShield-System.git
cd MarkShield-System

# 2. Run it
python main.py
```

On first launch, MarkShield sets itself up automatically — database, tables, and a default admin account, all ready to go.

| Username | Password   |
|----------|------------|
| `admin`  | `admin123` |

> Change the admin password after your first login.

---

## Who Uses MarkShield?

### Students
You finally have a voice. Log in to:
- View your marks and full mark history
- Check your GPA and academic standing
- Flag a mark that doesn't look right
- Track the status of your flags
- Do a wellness check-in when things get tough
- Stay updated with notifications

### Lecturers
Your workflow, simplified:
- Enter and manage student marks
- Request corrections when mistakes happen
- Track the status of your correction requests
- Get notified when requests are reviewed

### Academic Administrators
Full oversight, full control:
- Review and approve or reject correction requests
- Investigate flagged discrepancies
- Browse the complete audit trail
- Generate reports on GPA, course performance, and flag statistics
- Keep everyone informed through the notification system

---

## Project Structure

```
markshield/
├── main.py            # App entry point and all role menus
├── database.py        # Schema setup, seeding, and DB connection
├── auth.py            # Registration and login with SHA-256 hashing
├── marks.py           # Mark entry, flagging, corrections
├── gpa.py             # GPA calculation and academic summary
├── wellness.py        # Wellness check-ins and history
├── notifications.py   # Notification system
├── audit.py           # Audit trail logging and viewing
├── reports.py         # Admin report generation
├── config.py          # Grading scale and system constants
└── README.md
```

> `markshield.db` is auto-generated on first run and is excluded from version control — your data stays local.

---

## Under the Hood

MarkShield uses **SQLite** — lightweight, serverless, and perfect for a system like this.

| Table | What it stores |
|-------|----------------|
| `users` | All accounts — students, lecturers, admins |
| `marks` | Student marks with grades, credit hours, and lecturer info |
| `flags` | Discrepancy flags raised by students |
| `correction_requests` | Correction requests submitted by lecturers |
| `notifications` | Per-user inbox with read/unread status |
| `audit_trail` | Every action, timestamped and attributed |
| `wellness_checkins` | Student mood and stress records |

---

## Security

We take data integrity seriously:

- Passwords are hashed with **SHA-256** — never stored in plain text
- **Role-Based Access Control (RBAC)** — each role only sees what they're supposed to
- Every mark change is recorded in the **audit trail** — nothing gets quietly edited
- **Foreign key constraints** enforced at the database level

---

## Grading Scale

| Score | Grade | GPA Points |
|-------|-------|------------|
| 90–100 | A+   | 4.0 |
| 85–89  | A    | 4.0 |
| 80–84  | A-   | 3.7 |
| 75–79  | B+   | 3.3 |
| 70–74  | B    | 3.0 |
| 65–69  | B-   | 2.7 |
| 60–64  | C+   | 2.3 |
| 55–59  | C    | 2.0 |
| 50–54  | C-   | 1.7 |
| 45–49  | D    | 1.0 |
| 0–44   | F    | 0.0 |

---

## The Team — Group 20

Names:
1. Kuol Akech                     
2. Divin Manzi                  
3. Esther Konde
4. Umutesi Maureen
5. Karen Musangwa               

---

## Project Info

Built as part of the **Peer Learning Project (PLP) — Trimester 2**

> *MarkShield was built by students, for students. We know how much a single mark can mean — that's why we built a system that protects every single one.*
