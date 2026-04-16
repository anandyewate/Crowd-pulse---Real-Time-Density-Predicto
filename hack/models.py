import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from config import DB_NAME

def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            phone_number TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password, phone_number):
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute('INSERT INTO users (username, password_hash, phone_number) VALUES (?, ?, ?)',
                     (username, password_hash, phone_number))
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False # User already exists
    finally:
        conn.close()
    return success

def verify_user(username, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None
