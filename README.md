# MarkShield — Student Marks Protection System

A command-line, menu-driven Python application with SQLite for transparent and secure academic marks management.

---

## 🚀 Quick Start

**Requirements:** Python 3.7+ — no external packages needed (uses standard library only)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd markshield

# 2. Run the application
python main.py
```

On first run, a default admin account is automatically created:

| Username | Password  |
|----------|-----------|
| `admin`  | `admin123` |

---

## 📁 Project Structure

```
markshield/
├── main.py          # Entry point and menu controller
├── database.py      # DB connection, schema, and seeding
├── auth.py          # Registration and login (SHA-256 hashing)
├── marks.py         # Mark entry, flagging, and corrections
├── gpa.py           # GPA calculation and academic summary
├── wellness.py      # Wellness check-in and history
├── notifications.py # Notification generation and delivery
├── audit.py         # Audit trail logging and viewing
├── reports.py       # Admin report generation
├── config.py        # All system constants (grades, thresholds)
└── README.md
```

> `markshield.db` is auto-created on first run and is excluded from version control via `.gitignore`.

---

## 👥 Roles & Menus

### 🎓 Student
- View marks, GPA summary, and mark history
- Flag a mark discrepancy and track flag status
- Wellness check-in and history
- View notifications

### 👨‍🏫 Lecturer
- Enter student marks
- View submitted marks
- Request mark corrections and track their status
- View notifications

### 🛡️ Academic Administrator
- Review and approve/reject correction requests
- Investigate and resolve flagged discrepancies
- View full system audit trail
- Generate reports (GPA summary, course performance, flag stats)
- View notifications

---

## 🗄️ Database Schema

| Table | Purpose |
|-------|---------|
| `users` | All user accounts with hashed passwords and roles |
| `marks` | Student marks with grade, credit hours, and lecturer |
| `flags` | Student-raised discrepancy flags |
| `correction_requests` | Lecturer-submitted correction requests |
| `notifications` | Per-user notification inbox with read status |
| `audit_trail` | Timestamped log of all system actions |
| `wellness_checkins` | Student mood and stress check-in records |

---

## 🔐 Security

- Passwords hashed with **SHA-256** before storage
- **Role-Based Access Control (RBAC)** — users only see their own menus
- All mark changes logged in the **audit trail** with timestamp and actor
- SQLite **foreign key constraints** enforced

---

## 📊 Grading Scale

| Score | Grade | GPA Points |
|-------|-------|------------|
| 90–100 | A+ | 4.0 |
| 85–89  | A  | 4.0 |
| 80–84  | A- | 3.7 |
| 75–79  | B+ | 3.3 |
| 70–74  | B  | 3.0 |
| 65–69  | B- | 2.7 |
| 60–64  | C+ | 2.3 |
| 55–59  | C  | 2.0 |
| 50–54  | C- | 1.7 |
| 45–49  | D  | 1.0 |
| 0–44   | F  | 0.0 |

---

## 👨‍💻 Team

| Name | Student ID | GitHub |
|------|-----------|--------|
|      |           |        |
|      |           |        |
|      |           |        |

---

*Built as part of the Peer Learning Project (PLP) — Trimester 2*