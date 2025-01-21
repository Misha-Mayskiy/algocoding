# Создание словаря
my_dict = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Доступ к значениям
print(my_dict["name"])  # Вывод: Alice
print(my_dict.get("age"))  # Вывод: 30

# Изменение значений
my_dict["age"] = 31
print(my_dict)  # Вывод: {'name': 'Alice', 'age': 31, 'city': 'New York'}

# Добавление элементов
my_dict["email"] = "alice@example.com"
print(my_dict)  # Вывод: {'name': 'Alice', 'age': 31, 'city': 'New York', 'email': 'alice@example.com'}

# Удаление элементов
del my_dict["city"]
print(my_dict)  # Вывод: {'name': 'Alice', 'age': 31, 'email': 'alice@example.com'}

popped_value = my_dict.pop("age")
print(popped_value)  # Вывод: 31
print(my_dict)  # Вывод: {'name': 'Alice', 'email': 'alice@example.com'}

my_dict.popitem()
print(my_dict)  # Вывод: {'name': 'Alice'}

my_dict.clear()
print(my_dict)  # Вывод: {}

# Проверка наличия ключа
my_dict = {"name": "Alice", "age": 30, "city": "New York"}
print("name" in my_dict)  # Вывод: True

# Получение всех ключей, значений и пар
print(my_dict.keys())  # Вывод: dict_keys(['name', 'age', 'city'])
print(my_dict.values())  # Вывод: dict_values(['Alice', 30, 'New York'])
print(my_dict.items())  # Вывод: dict_items([('name', 'Alice'), ('age', 30), ('city', 'New York')])

# Копирование словаря
new_dict = my_dict.copy()
print(new_dict)  # Вывод: {'name': 'Alice', 'age': 30, 'city': 'New York'}

new_dict = dict(my_dict)
print(new_dict)  # Вывод: {'name': 'Alice', 'age': 30, 'city': 'New York'}

# Объединение словарей
another_dict = {"email": "alice@example.com", "phone": "123-456-7890"}
combined_dict = {**my_dict, **another_dict}
print(combined_dict)  # Вывод: {'name': 'Alice', 'age': 30, 'city': 'New York', 'email': 'alice@example.com', 'phone': '123-456-7890'}

my_dict.update(another_dict)
print(my_dict)  # Вывод: {'name': 'Alice', 'age': 30, 'city': 'New York', 'email': 'alice@example.com', 'phone': '123-456-7890'}
