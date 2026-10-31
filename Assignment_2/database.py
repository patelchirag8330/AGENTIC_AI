"""SQLite setup. All queries elsewhere use ? parameters (no string-built SQL)."""
import sqlite3
import config
from werkzeug.security import generate_password_hash, check_password_hash

SCHEMA = """
CREATE TABLE IF NOT EXISTS students(student_id TEXT PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS fees(student_id TEXT PRIMARY KEY REFERENCES students(student_id),
    fee_total INTEGER NOT NULL, fee_paid INTEGER NOT NULL, due_date TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS scholarships(student_id TEXT PRIMARY KEY REFERENCES students(student_id),
    status TEXT NOT NULL, detail TEXT);
CREATE TABLE IF NOT EXISTS tickets(ticket_id TEXT PRIMARY KEY, student_id TEXT NOT NULL REFERENCES students(student_id),
    category TEXT NOT NULL, description TEXT NOT NULL, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS memory(memory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id TEXT NOT NULL REFERENCES students(student_id), key TEXT NOT NULL, value TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(student_id, key));
CREATE TABLE IF NOT EXISTS credentials(student_id TEXT PRIMARY KEY REFERENCES students(student_id), password_hash TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS contacts(student_id TEXT PRIMARY KEY REFERENCES students(student_id),
    email TEXT NOT NULL, phone TEXT NOT NULL);
-- A sensitive change is only a REQUEST until the student confirms it (Approve button). status: pending -> executed | rejected
CREATE TABLE IF NOT EXISTS approvals(approval_id TEXT PRIMARY KEY, student_id TEXT NOT NULL REFERENCES students(student_id),
    field TEXT NOT NULL CHECK(field IN ('email','phone')), old_value TEXT, new_value TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','executed','rejected')),
    requested_at TEXT DEFAULT CURRENT_TIMESTAMP, decided_by TEXT, decided_at TEXT, note TEXT);
-- Audit log: who, what, allowed?, result. Each row stores a hash of the previous row (tamper evidence).
CREATE TABLE IF NOT EXISTS audit_log(audit_id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT NOT NULL,
    actor_id TEXT NOT NULL, actor_role TEXT NOT NULL, action TEXT NOT NULL, target TEXT, details TEXT,
    decision TEXT NOT NULL, result TEXT NOT NULL, session_id TEXT, prev_hash TEXT NOT NULL, row_hash TEXT NOT NULL);
CREATE TRIGGER IF NOT EXISTS audit_no_update BEFORE UPDATE ON audit_log BEGIN SELECT RAISE(ABORT, 'audit log is append-only'); END;
CREATE TRIGGER IF NOT EXISTS audit_no_delete BEFORE DELETE ON audit_log BEGIN SELECT RAISE(ABORT, 'audit log is append-only'); END;
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor_id);
CREATE INDEX IF NOT EXISTS idx_mem ON memory(student_id);
"""


def connect(db_path=None):
    conn = sqlite3.connect(db_path or config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path=None, reset=False):
    conn = connect(db_path)
    if reset:
        for table in ("approvals", "audit_log", "contacts", "credentials", "memory", "tickets", "scholarships", "fees", "students"):
            conn.execute(f"DROP TABLE IF EXISTS {table}")
    conn.executescript(SCHEMA)
    conn.close()


def add_student(student_id, name, password, fee_total=0, fee_paid=0,
                due_date="", scholarship_status="none", scholarship_detail="",
                email="", phone="", db_path=None):
    """Provision one real account. Passwords are stored only as salted hashes."""
    sid = student_id.strip().upper()
    if not sid or not name.strip() or len(password) < 8:
        raise ValueError("Student ID, name and a password of at least 8 characters are required.")
    conn = connect(db_path)
    try:
        with conn:
            conn.execute("INSERT INTO students VALUES(?,?)", (sid, name.strip()))
            conn.execute("INSERT INTO credentials VALUES(?,?)",
                         (sid, generate_password_hash(password)))
            conn.execute("INSERT INTO fees VALUES(?,?,?,?)",
                         (sid, int(fee_total), int(fee_paid), due_date or ""))
            conn.execute("INSERT INTO scholarships VALUES(?,?,?)",
                         (sid, scholarship_status, scholarship_detail))
            conn.execute("INSERT INTO contacts VALUES(?,?,?)", (sid, email, phone))
    finally:
        conn.close()


def list_students(db_path=None):
    """Return student IDs and names for privacy checks; never return credentials or contact data."""
    conn = connect(db_path)
    try:
        rows = conn.execute("SELECT student_id, name FROM students ORDER BY student_id").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def verify_login(student_id, password, db_path=None):
    conn = connect(db_path)
    row = conn.execute("SELECT password_hash FROM credentials WHERE student_id=?", (student_id,)).fetchone()
    conn.close()
    return bool(row) and check_password_hash(row["password_hash"], password)


def student_name(student_id, db_path=None):
    conn = connect(db_path)
    row = conn.execute("SELECT name FROM students WHERE student_id=?", (student_id,)).fetchone()
    conn.close()
    return row["name"] if row else None


if __name__ == "__main__":
    import getpass
    init_db()
    sid, name = input("Student ID: "), input("Student name: ")
    password = getpass.getpass("Password (8+ characters): ")
    total = int(input("Total fee (0 if not set): ") or 0)
    paid = int(input("Fee paid (0 if not set): ") or 0)
    email, phone = input("Email: "), input("Phone: ")
    add_student(sid, name, password, total, paid, email=email, phone=phone)
    print("Account created.")
