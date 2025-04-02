import sqlite3
from app.config import settings
from datetime import datetime

conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
cur = conn.cursor()

def initialize_history_store():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        session_id TEXT,
        prompt TEXT,
        response TEXT,
        created_at TEXT
    )
    """)
    conn.commit()

def store_history(user_id: str, session_id: str, prompt: str, response: str):
    cur.execute("INSERT INTO history (user_id, session_id, prompt, response, created_at) VALUES (?, ?, ?, ?, ?)",
                (user_id, session_id, prompt, response, datetime.utcnow().isoformat()))
    conn.commit()

def get_history(user_id: str, session_id: str):
    cur.execute("SELECT prompt, response FROM history WHERE user_id = ? AND session_id = ? ORDER BY created_at ASC",
                (user_id, session_id))
    rows = cur.fetchall()
    return [{"prompt": row[0], "response": row[1]} for row in rows]

def count_history(user_id: str, session_id: str) -> int:
    cur.execute("SELECT COUNT(*) FROM history WHERE user_id = ? AND session_id = ?", (user_id, session_id))
    return cur.fetchone()[0]
