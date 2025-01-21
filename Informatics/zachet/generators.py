# Генераторы в Python

# Генераторные выражения

# Пример создания генераторного выражения
gen_expr = (x * x for x in range(10))

# Итерация по генератору
for value in gen_expr:
    print(value)

# Использование генератора с функцией sum
total = sum(x * x for x in range(10))
print(total)  # Вывод: 285

# Использование генераторов в списках

# 1. Создание списка с помощью генераторного выражения
squares = [x * x for x in range(10)]
print(squares)  # Вывод: [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# 2. Фильтрация элементов списка
even_numbers = [x for x in range(10) if x % 2 == 0]
print(even_numbers)  # Вывод: [0, 2, 4, 6, 8]

# 3. Преобразование элементов списка
words = ["hello", "world", "python"]
uppercase_words = [word.upper() for word in words]
print(uppercase_words)  # Вывод: ['HELLO', 'WORLD', 'PYTHON']

# 4. Вложенные генераторные выражения
pairs = [(i, j) for i in range(3) for j in range(3)]
print(pairs)  # Вывод: [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]

# 5. Использование генераторной функции для создания списка
def number_sequence(n):
    for i in range(n):
        yield i

# Создание списка с помощью генераторной функции
sequence = list(number_sequence(5))
print(sequence)  # Вывод: [0, 1, 2, 3, 4]
