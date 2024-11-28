# generate_tasks_queries.py

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

# Ініціалізуємо Faker
fake = Faker()

# Підключення до бази даних
conn = psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
cur = conn.cursor()

# Отримуємо всі доступні user_id та task_id
cur.execute("SELECT id FROM users")
user_ids = [row[0] for row in cur.fetchall()]

cur.execute("SELECT id FROM tasks")
task_ids = [row[0] for row in cur.fetchall()]

# Якщо списки порожні, виводимо повідомлення
if not user_ids:
    print("Таблиця users порожня. Будь ласка, заповніть її перед запуском цього скрипту.")
    exit()

if not task_ids:
    print("Таблиця tasks порожня. Будь ласка, заповніть її перед запуском цього скрипту.")
    exit()

# Вибираємо випадкові user_id та task_id
random_user_id = random.choice(user_ids)
random_task_id = random.choice(task_ids)

# Генеруємо випадковий домен для пошти
email_domain = fake.free_email_domain()
email_pattern = f'%@{email_domain}'

# Формуємо вміст файлу tasks_queries.sql
sql_queries = f"""
-- tasks_queries.sql

-- 1. Отримати всі завдання користувача з id = {random_user_id}
SELECT * FROM tasks
WHERE user_id = {random_user_id};

-- 2. Вибрати завдання за статусом 'new'
SELECT * FROM tasks
WHERE status_id = (
    SELECT id FROM status WHERE name = 'new'
);

-- 3. Оновити статус завдання з id = {random_task_id}
UPDATE tasks
SET status_id = (
    SELECT id FROM status WHERE name = 'in progress'
)
WHERE id = {random_task_id};

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id FROM tasks
);

-- 5. Додати нове завдання для користувача з id = {random_user_id}
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    '{fake.sentence(nb_words=6).replace("'", "''")}',
    '{fake.text(max_nb_chars=200).replace("'", "''")}',
    (SELECT id FROM status WHERE name = 'new'),
    {random_user_id}
);

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks
WHERE status_id != (
    SELECT id FROM status WHERE name = 'completed'
);

-- 7. Видалити завдання з id = {random_task_id}
DELETE FROM tasks
WHERE id = {random_task_id};

-- 8. Знайти користувачів з певною електронною поштою
-- Використаємо домен '{email_domain}'
SELECT * FROM users
WHERE email LIKE '%@{email_domain}';

-- 9. Оновити ім'я користувача з id = {random_user_id}
UPDATE users
SET fullname = '{fake.name().replace("'", "''")}'
WHERE id = {random_user_id};

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Отримати завдання, призначені користувачам з доменом '{email_domain}'
SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@{email_domain}';

-- 12. Отримати список завдань, що не мають опису
SELECT * FROM tasks
WHERE description IS NULL OR description = '';

-- 13. Вибрати користувачів та їхні завдання у статусі 'in progress'
SELECT u.fullname, t.title, s.name AS status_name
FROM users u
JOIN tasks t ON u.id = t.user_id
JOIN status s ON t.status_id = s.id
WHERE s.name = 'in progress';

-- 14. Отримати користувачів та кількість їхніх завдань
SELECT u.fullname, COUNT(t.id) AS task_count
FROM users u
LEFT JOIN tasks t ON u.id = t.user_id
GROUP BY u.fullname;
"""

# Записуємо SQL-запити у файл tasks_queries.sql
with open('tasks_queries.sql', 'w', encoding='utf-8') as f:
    f.write(sql_queries)

print("Файл tasks_queries.sql успішно створено.")

# Закриваємо з'єднання
cur.close()
conn.close()
