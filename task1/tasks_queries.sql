
-- tasks_queries.sql

-- 1. Отримати всі завдання користувача з id = 10
SELECT * FROM tasks
WHERE user_id = 10;

-- 2. Вибрати завдання за статусом 'new'
SELECT * FROM tasks
WHERE status_id = (
    SELECT id FROM status WHERE name = 'new'
);

-- 3. Оновити статус завдання з id = 8
UPDATE tasks
SET status_id = (
    SELECT id FROM status WHERE name = 'in progress'
)
WHERE id = 8;

-- 4. Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users
WHERE id NOT IN (
    SELECT DISTINCT user_id FROM tasks
);

-- 5. Додати нове завдання для користувача з id = 10
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'Meeting civil deep.',
    'Note newspaper party something national herself war make. Education win type she.
Art size protect smile. Sort later so discover all near set happy.
Process admit those best far cup dog skin.',
    (SELECT id FROM status WHERE name = 'new'),
    10
);

-- 6. Отримати всі завдання, які ще не завершено
SELECT * FROM tasks
WHERE status_id != (
    SELECT id FROM status WHERE name = 'completed'
);

-- 7. Видалити завдання з id = 8
DELETE FROM tasks
WHERE id = 8;

-- 8. Знайти користувачів з певною електронною поштою
-- Використаємо домен 'gmail.com'
SELECT * FROM users
WHERE email LIKE '%@gmail.com';

-- 9. Оновити ім'я користувача з id = 10
UPDATE users
SET fullname = 'Crystal Williams'
WHERE id = 10;

-- 10. Отримати кількість завдань для кожного статусу
SELECT s.name AS status_name, COUNT(t.id) AS task_count
FROM status s
LEFT JOIN tasks t ON s.id = t.status_id
GROUP BY s.name;

-- 11. Отримати завдання, призначені користувачам з доменом 'gmail.com'
SELECT t.*
FROM tasks t
JOIN users u ON t.user_id = u.id
WHERE u.email LIKE '%@gmail.com';

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
