import sqlite3


conn = sqlite3.connect("not_telegram.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER,
    balance INTEGER NOT NULL
)
''')

cursor.execute('''
DELETE FROM Users
''')

for i in range(1, 11):
    username = f"User{i}"
    email = f"example{i}@gmail.com"
    age = i * 10
    balance = 1000
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)", (username, email, age, balance))

cursor.execute("UPDATE Users SET balance = 500 WHERE id % 2 = 1")

cursor.execute("DELETE FROM Users WHERE (id + 2) % 3 = 0")

cursor.execute("DELETE FROM Users WHERE id = 6")

cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]

cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]

print(all_balances / total_users)

cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60")
rows = cursor.fetchall()

for row in rows:
    print(f"Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}")

conn.commit()
conn.close()
