# seed.py

import psycopg2
from psycopg2 import sql
from faker import Faker
import random

# Параметри підключення до бази даних
DB_NAME = 'your_database_name'
DB_USER = 'vmikhidenko'
DB_PASSWORD = '123456'
DB_HOST = 'localhost'
DB_PORT = '5432'

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Ініціалізуємо Faker
fake = Faker()

# Дані для таблиці status
status_list = ['new', 'in progress', 'completed']

# Заповнюємо таблицю status
for status_name in status_list:
    cur.execute("""
        INSERT INTO status (name) VALUES (%s)
        ON CONFLICT (name) DO NOTHING
    """, (status_name,))
conn.commit()

# Отримуємо id статусів
cur.execute("SELECT id, name FROM status")
status_dict = {name: id for id, name in cur.fetchall()}

# Створюємо користувачів
users = []
for _ in range(10):  # Створимо 10 користувачів
    fullname = fake.name()
    email = fake.unique.email()
    users.append((fullname, email))
cur.executemany("""
    INSERT INTO users (fullname, email) VALUES (%s, %s)
    ON CONFLICT (email) DO NOTHING
""", users)
conn.commit()

# Отримуємо id користувачів
cur.execute("SELECT id FROM users")
user_ids = [id for (id,) in cur.fetchall()]

# Створюємо завдання
tasks = []
for _ in range(30):  # Створимо 30 завдань
    title = fake.sentence(nb_words=6).replace("'", "''")
    description = fake.text(max_nb_chars=200).replace("'", "''")
    status_id = random.choice(list(status_dict.values()))
    user_id = random.choice(user_ids)
    tasks.append((title, description, status_id, user_id))
cur.executemany("""
    INSERT INTO tasks (title, description, status_id, user_id)
    VALUES (%s, %s, %s, %s)
""", tasks)
conn.commit()

# Закриття з'єднання
cur.close()
conn.close()
