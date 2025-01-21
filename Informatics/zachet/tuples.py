# Создание кортежа
my_tuple = (1, 2, 3, 4, 5)

# Доступ к элементам
print(my_tuple[0])  # Вывод: 1
print(my_tuple[1:3])  # Вывод: (2, 3)

# Объединение кортежей
another_tuple = (6, 7, 8)
combined_tuple = my_tuple + another_tuple
print(combined_tuple)  # Вывод: (1, 2, 3, 4, 5, 6, 7, 8)

# Повторение кортежей
repeated_tuple = my_tuple * 3
print(repeated_tuple)  # Вывод: (1, 2, 3, 4, 5, 1, 2, 3, 4, 5, 1, 2, 3, 4, 5)

# Поиск элементов
index = my_tuple.index(4)
print(index)  # Вывод: 3

count = my_tuple.count(2)
print(count)  # Вывод: 1

# Преобразование в список и обратно
my_list = list(my_tuple)
print(my_list)  # Вывод: [1, 2, 3, 4, 5]

my_tuple = tuple(my_list)
print(my_tuple)  # Вывод: (1, 2, 3, 4, 5)

# Распаковка кортежей
a, b, c, d, e = my_tuple
print(a, b, c, d, e)  # Вывод: 1 2 3 4 5
