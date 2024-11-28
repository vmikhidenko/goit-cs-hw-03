from pymongo import MongoClient, errors
import sys

def get_database():
    """
    Створює з'єднання з MongoDB та повертає об'єкт бази даних.
    """
    try:
        # Підключення до локального сервера MongoDB
        client = MongoClient('mongodb://localhost:27017/')
        db = client['cat_database']
        return db
    except errors.ConnectionFailure as e:
        print(f"Не вдалося підключитися до MongoDB: {e}")
        sys.exit(1)

def insert_cat(db, cat_data):
    """
    Додає новий документ (кота) до колекції.
    """
    try:
        result = db.cats.insert_one(cat_data)
        print(f"Кот доданий з _id: {result.inserted_id}")
    except errors.PyMongoError as e:
        print(f"Помилка при додаванні кота: {e}")

def get_all_cats(db):
    """
    Виводить всі документи з колекції.
    """
    try:
        cats = db.cats.find()
        for cat in cats:
            print(cat)
    except errors.PyMongoError as e:
        print(f"Помилка при отриманні котів: {e}")

def get_cat_by_name(db, name):
    """
    Виводить інформацію про кота за його ім'ям.
    """
    try:
        cat = db.cats.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кот з ім'ям '{name}' не знайдений.")
    except errors.PyMongoError as e:
        print(f"Помилка при пошуку кота: {e}")

def update_cat_age(db, name, new_age):
    """
    Оновлює вік кота за його ім'ям.
    """
    try:
        result = db.cats.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота '{name}' оновлено до {new_age}.")
        else:
            print(f"Кот з ім'ям '{name}' не знайдений або вік той самий.")
    except errors.PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

def add_feature_to_cat(db, name, feature):
    """
    Додає нову характеристику до списку features кота за ім'ям.
    """
    try:
        result = db.cats.update_one(
            {"name": name},
            {"$push": {"features": feature}}
        )
        if result.modified_count > 0:
            print(f"Характеристика '{feature}' додана коту '{name}'.")
        else:
            print(f"Кот з ім'ям '{name}' не знайдений.")
    except errors.PyMongoError as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

def delete_cat_by_name(db, name):
    """
    Видаляє запис про кота за його ім'ям.
    """
    try:
        result = db.cats.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кот з ім'ям '{name}' видалений.")
        else:
            print(f"Кот з ім'ям '{name}' не знайдений.")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

def delete_all_cats(db):
    """
    Видаляє всі записи з колекції.
    """
    try:
        result = db.cats.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except errors.PyMongoError as e:
        print(f"Помилка при видаленні всіх котів: {e}")

def main():
    db = get_database()

    while True:
        print("\nВиберіть опцію:")
        print("1. Додати нового кота")
        print("2. Вивести всіх котів")
        print("3. Знайти кота за ім'ям")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота за ім'ям")
        print("7. Видалити всіх котів")
        print("8. Вийти")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            name = input("Введіть ім'я кота: ")
            age = int(input("Введіть вік кота: "))
            features = input("Введіть характеристики кота (через кому): ").split(',')
            cat_data = {
                "name": name,
                "age": age,
                "features": [feature.strip() for feature in features]
            }
            insert_cat(db, cat_data)

        elif choice == '2':
            get_all_cats(db)

        elif choice == '3':
            name = input("Введіть ім'я кота для пошуку: ")
            get_cat_by_name(db, name)

        elif choice == '4':
            name = input("Введіть ім'я кота для оновлення віку: ")
            new_age = int(input("Введіть новий вік кота: "))
            update_cat_age(db, name, new_age)

        elif choice == '5':
            name = input("Введіть ім'я кота для додавання характеристики: ")
            feature = input("Введіть нову характеристику: ")
            add_feature_to_cat(db, name, feature)

        elif choice == '6':
            name = input("Введіть ім'я кота для видалення: ")
            delete_cat_by_name(db, name)

        elif choice == '7':
            confirm = input("Ви впевнені, що хочете видалити всіх котів? (y/n): ")
            if confirm.lower() == 'y':
                delete_all_cats(db)

        elif choice == '8':
            print("Вихід.")
            break

        else:
            print("Невірний вибір. Спробуйте ще раз.")

if __name__ == "__main__":
    main()
