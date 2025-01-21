import sqlite3


def initiate_db():
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            price INTEGER NOT NULL,
            image TEXT NOT NULL
        )
    """)
    conn = sqlite3.connect("products.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT NOT NULL,
            age INTEGER NOT NULL,
            balance INTEGER NOT NULL DEFAULT 1000
        )
    """)
    conn.commit()
    conn.close()


def add_user(username, email, age):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO Users (username, email, age, balance) 
        VALUES (?, ?, ?, 1000)
    """, (username, email, age))
    connection.commit()
    connection.close()


def is_included(username):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
    user = cursor.fetchone()
    connection.close()
    return user is not None


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT id, title, description, price, image FROM Products")
    products = cursor.fetchall()
    connection.close()
    return products
