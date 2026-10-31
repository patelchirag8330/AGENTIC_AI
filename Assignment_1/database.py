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
        for table in ("credentials", "memory", "tickets", "scholarships", "fees", "students"):
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
