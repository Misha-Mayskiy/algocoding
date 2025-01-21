# Создание списка
my_list = [1, 2, 3, 4, 5]

# Доступ к элементам
print(my_list[0])  # Вывод: 1
print(my_list[1:3])  # Вывод: [2, 3]

# Изменение элементов
my_list[0] = 10
print(my_list)  # Вывод: [10, 2, 3, 4, 5]

# Добавление элементов
my_list.append(6)
print(my_list)  # Вывод: [10, 2, 3, 4, 5, 6]

my_list.insert(2, 7)
print(my_list)  # Вывод: [10, 2, 7, 3, 4, 5, 6]

my_list.extend([8, 9])
print(my_list)  # Вывод: [10, 2, 7, 3, 4, 5, 6, 8, 9]

# Удаление элементов
my_list.remove(3)
print(my_list)  # Вывод: [10, 2, 7, 4, 5, 6, 8, 9]

popped_element = my_list.pop(1)
print(popped_element)  # Вывод: 2
print(my_list)  # Вывод: [10, 7, 4, 5, 6, 8, 9]

my_list.clear()
print(my_list)  # Вывод: []

# Поиск элементов
my_list = [1, 2, 3, 4, 5]
index = my_list.index(4)
print(index)  # Вывод: 3

count = my_list.count(2)
print(count)  # Вывод: 1

# Сортировка
my_list.sort()
print(my_list)  # Вывод: [1, 2, 3, 4, 5]

my_list.sort(reverse=True)
print(my_list)  # Вывод: [5, 4, 3, 2, 1]

# Копирование списка
new_list = my_list.copy()
print(new_list)  # Вывод: [5, 4, 3, 2, 1]

new_list = my_list[:]
print(new_list)  # Вывод: [5, 4, 3, 2, 1]

# Объединение списков
another_list = [6, 7, 8]
combined_list = my_list + another_list
print(combined_list)  # Вывод: [5, 4, 3, 2, 1, 6, 7, 8]
