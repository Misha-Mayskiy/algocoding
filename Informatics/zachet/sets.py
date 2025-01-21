# Создание множества
my_set = {1, 2, 3, 4, 5}

# Добавление элементов
my_set.add(6)
print(my_set)  # Вывод: {1, 2, 3, 4, 5, 6}

my_set.update([7, 8])
print(my_set)  # Вывод: {1, 2, 3, 4, 5, 6, 7, 8}

# Удаление элементов
my_set.remove(3)
print(my_set)  # Вывод: {1, 2, 4, 5, 6, 7, 8}

my_set.discard(9)  # Ничего не произойдет, так как 9 нет в множестве
print(my_set)  # Вывод: {1, 2, 4, 5, 6, 7, 8}

popped_element = my_set.pop()
print(popped_element)  # Вывод: произвольный элемент из множества
print(my_set)  # Вывод: множество без удаленного элемента

my_set.clear()
print(my_set)  # Вывод: set()

# Операции множеств
my_set = {1, 2, 3, 4, 5}
another_set = {4, 5, 6, 7, 8}

union_set = my_set | another_set
print(union_set)  # Вывод: {1, 2, 3, 4, 5, 6, 7, 8}

intersection_set = my_set & another_set
print(intersection_set)  # Вывод: {4, 5}

difference_set = my_set - another_set
print(difference_set)  # Вывод: {1, 2, 3}

sym_diff_set = my_set ^ another_set
print(sym_diff_set)  # Вывод: {1, 2, 3, 6, 7, 8}

# Проверка наличия элемента
print(3 in my_set)  # Вывод: True

# Копирование множества
new_set = my_set.copy()
print(new_set)  # Вывод: {1, 2, 3, 4, 5}
