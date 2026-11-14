import sqlite3
import bcrypt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "interview_coach.db")

def create_connection():
    os.makedirs(BASE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    return conn



def create_table():
    conn = create_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    # Interview History Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interview_history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            interview_date TEXT,
            score TEXT,
            report TEXT
        )
    """)

    conn.commit()
    conn.close()

def register_user(name, email, password):
    conn = create_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        cursor.execute(
            "INSERT INTO users(name,email,password) VALUES(?,?,?)",
            (name, email, hashed_password)
        )
        conn.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        conn.close()


def login_user(email, password):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        if bcrypt.checkpw(password.encode(), user[3]):
            return user

    return None

from datetime import datetime

def save_interview(email, score, report):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interview_history(email, interview_date, score, report)
    VALUES (?, ?, ?, ?)
    """, (
        email,
        datetime.now().strftime("%d-%m-%Y %H:%M"),
        score,
        report
    ))

    conn.commit()
    conn.close()

def get_interview_history(email):

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT interview_date, score, report
        FROM interview_history
        WHERE email = ?
        ORDER BY id DESC
    """, (email,))

    data = cursor.fetchall()

    conn.close()

    return data