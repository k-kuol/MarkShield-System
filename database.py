import sqlite3
import os
import hashlib

DB_PATH = os.path.join(os.path.dirname(__file__), "markshield.db")


def _hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('student', 'lecturer', 'admin')),
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS marks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_username TEXT NOT NULL,
                course_code TEXT NOT NULL,
                course_name TEXT NOT NULL,
                credit_hours INTEGER NOT NULL,
                score REAL NOT NULL,
                grade TEXT NOT NULL,
                entered_by TEXT NOT NULL,
                entered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_username) REFERENCES users(username),
                FOREIGN KEY (entered_by) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS flags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_username TEXT NOT NULL,
                mark_id INTEGER NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'resolved', 'rejected')),
                flagged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_by TEXT,
                resolved_at TIMESTAMP,
                resolution_note TEXT,
                FOREIGN KEY (student_username) REFERENCES users(username),
                FOREIGN KEY (mark_id) REFERENCES marks(id)
            );

            CREATE TABLE IF NOT EXISTS correction_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mark_id INTEGER NOT NULL,
                requested_by TEXT NOT NULL,
                old_score REAL NOT NULL,
                new_score REAL NOT NULL,
                reason TEXT NOT NULL,
                status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'approved', 'rejected')),
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_by TEXT,
                reviewed_at TIMESTAMP,
                FOREIGN KEY (mark_id) REFERENCES marks(id),
                FOREIGN KEY (requested_by) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                message TEXT NOT NULL,
                is_read INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (username) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS audit_trail (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                performed_by TEXT NOT NULL,
                action TEXT NOT NULL,
                details TEXT,
                performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (performed_by) REFERENCES users(username)
            );

            CREATE TABLE IF NOT EXISTS wellness_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_username TEXT NOT NULL,
                mood_score INTEGER NOT NULL CHECK(mood_score BETWEEN 1 AND 10),
                stress_level INTEGER NOT NULL CHECK(stress_level BETWEEN 1 AND 10),
                notes TEXT,
                checked_in_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_username) REFERENCES users(username)
            );
        """)

def seed_demo_data():
    """Insert a default admin account if no users exist yet."""
    with get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO users (username, password_hash, role, full_name) VALUES (?, ?, ?, ?)",
                ("admin", _hash("admin123"), "admin", "System Administrator")
            )
            conn.execute(
                "INSERT INTO notifications (username, message) VALUES (?, ?)",
                ("admin", "Welcome to MarkShield! Default admin account created. Please change your password.")
            )
            print("  [Setup] Default admin created — username: admin / password: admin123")