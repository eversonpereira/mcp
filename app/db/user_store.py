import sqlite3
from app.config import settings

conn = sqlite3.connect(settings.DB_PATH, check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
)
""")
conn.commit()

import uuid

def create_user(username: str, password: str):
    uid = str(uuid.uuid4())
    cur.execute("INSERT INTO users (id, username, password) VALUES (?, ?, ?)", (uid, username, password))
    conn.commit()

def get_user_by_username(username: str):
    cur.execute("SELECT id, username, password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None

def get_user_by_id(user_id: str):
    cur.execute("SELECT id, username, password FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    if row:
        return {"id": row[0], "username": row[1], "password": row[2]}
    return None
