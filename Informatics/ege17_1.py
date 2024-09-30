# Чтение файла и извлечение последовательности чисел
file_path = '17_1.txt'

# Чтение данных
with open(file_path, 'r') as file:
    data = file.readlines()

# Преобразование данных в список целых чисел
sequence = [int(num.strip()) for num in data]

# Найдем двух минимальных положительных элементов, кратных 17, и максимальный элемент, оканчивающийся на 69
positive_17_multiples = sorted([x for x in sequence if x > 0 and x % 17 == 0])
min1, min2 = positive_17_multiples[:2] if len(positive_17_multiples) >= 2 else (0, 0)

max_ending_69 = max([x for x in sequence if x % 100 == 69], default=0)

# Теперь можно приступить к поиску четверок с учетом всех условий
results = []
for i in range(len(sequence) - 3):
    quad = sequence[i:i + 4]

    # Проверяем условия
    three_digit_count = sum(100 <= abs(x) <= 999 for x in quad)
    divisible_by_18 = sum(x % 18 == 0 for x in quad)
    sum_divisible_by_min_sum = sum(quad) % (min1 + min2) == 0 if (min1 + min2) > 0 else False
    product_within_limit = (quad[0] * quad[1] * quad[2] * quad[3]) <= (max_ending_69 ** 2)

    if three_digit_count == 2 and divisible_by_18 == 1 and sum_divisible_by_min_sum and product_within_limit:
        results.append(sum(quad) ** 2)

# Результат: количество найденных четверок и минимальный квадрат суммы
count_of_quads = len(results)
min_square_sum = min(results) if results else None

print(count_of_quads, min_square_sum)
