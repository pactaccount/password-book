import sqlite3
import hashlib

def create_table():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            website TEXT NOT NULL,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    # You should use a stronger hashing algorithm in a real-world application
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(website, username, password):
    hashed_password = hash_password(password)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO passwords (website, username, password)
        VALUES (?, ?, ?)
    ''', (website, username, hashed_password))
    conn.commit()
    conn.close()

def get_passwords():
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passwords')
    passwords = cursor.fetchall()
    conn.close()

    return passwords

def update_password(password_id, new_password):
    hashed_password = hash_password(new_password)

    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE passwords
        SET password = ?
        WHERE id = ?
    ''', (hashed_password, password_id))
    conn.commit()
    conn.close()

def delete_password(password_id):
    conn = sqlite3.connect("passwords.db")
    cursor = conn.cursor()
    cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
    conn.commit()
    conn.close()
