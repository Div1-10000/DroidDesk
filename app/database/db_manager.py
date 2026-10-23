import sqlite3
from pathlib import Path

class DBManager:
    def __init__(self, path=None):
        self.path = Path(path) if path else Path(__file__).resolve().parents[2] / "data" / "droiddesk.db"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                event_type TEXT NOT NULL,
                details TEXT NOT NULL
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )""")

    def connect(self):
        return sqlite3.connect(self.path)

    def log(self, event_type: str, details: str):
        # Keep logs operational; callers should never pass private phone content.
        with self.connect() as db:
            db.execute("INSERT INTO events(event_type, details) VALUES (?, ?)", (event_type, details))

    def get_setting(self, key: str, default: str = "") -> str:
        with self.connect() as db:
            row = db.execute("SELECT value FROM settings WHERE key=?", (key,)).fetchone()
            return row[0] if row else default

    def set_setting(self, key: str, value: str):
        with self.connect() as db:
            db.execute("INSERT INTO settings(key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                       (key, value))

    def recent_events(self, limit=50):
        with self.connect() as db:
            return db.execute("SELECT created_at, event_type, details FROM events ORDER BY id DESC LIMIT ?",
                              (limit,)).fetchall()
