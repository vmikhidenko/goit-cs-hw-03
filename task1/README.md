# goit-cs-hw-03
Інструкції використання:

Створіть базу даних та користувача:

Виконайте скрипт create_tables.sql:

psql -U your_username -d your_database_name -f create_tables.sql
Запустіть скрипт seed.py:

python seed.py
Це заповнить ваші таблиці випадковими даними.

Запустіть скрипт generate_tasks_queries.py:

python generate_tasks_queries.py
Це створить файл tasks_queries.sql з запитами.

Виконайте запити з файлу tasks_queries.sql:

Ви можете виконати їх через SQL-клієнт або командний рядок.

psql -U your_username -d your_database_name -f tasks_queries.sql
