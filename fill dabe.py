import sqlite3

connection = sqlite3.connect("products.db")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    price INTEGER NOT NULL,
    image TEXT NOT NULL
)
""")

cursor.execute("DELETE FROM Products")
cursor.execute("DELETE FROM sqlite_sequence WHERE name='Products'")

products_data = [
    ("Путешествие", "Описание путешествия", 100, "путешествие.jpg"),
    ("Силач", "Описание силача", 200, "силач.jpg"),
    ("Таблетки", "Описание таблеток", 300, "таблетки.jpg"),
    ("Ящеры", "Описание ящеров", 400, "ящеры.jpg")
]

cursor.executemany("INSERT INTO Products (title, description, price, image) VALUES (?, ?, ?, ?)", products_data)

connection.commit()
connection.close()

print("Данные успешно добавлены в таблицу Products.")
