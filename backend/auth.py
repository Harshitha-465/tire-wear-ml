import os
import sqlite3
import secrets
import hashlib
import hmac

DB_PATH = os.path.join("data", "users.db")

def init_db(db_path: str = DB_PATH) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT,
            salt BLOB NOT NULL,
            password_hash BLOB NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );
        """
    )
    conn.commit()
    conn.close()

def _hash_password(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        200_000
    )

def create_user(username: str, password: str, email: str | None = None, db_path: str = DB_PATH):
    init_db(db_path)
    username = username.strip()
    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    salt = secrets.token_bytes(16)
    pw_hash = _hash_password(password, salt)

    conn = sqlite3.connect(db_path)
    try:
        conn.execute(
            "INSERT INTO users(username, email, salt, password_hash) VALUES(?,?,?,?)",
            (username, email, salt, pw_hash)
        )
        conn.commit()
        return True, None
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    finally:
        conn.close()

def verify_user(username: str, password: str, db_path: str = DB_PATH) -> bool:
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT salt, password_hash FROM users WHERE username=?",
        (username.strip(),)
    ).fetchone()
    conn.close()

    if not row:
        return False

    salt, stored_hash = row
    calc_hash = _hash_password(password, salt)
    return hmac.compare_digest(calc_hash, stored_hash)