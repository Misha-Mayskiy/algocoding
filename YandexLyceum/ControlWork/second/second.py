import os
import statistics
import sys

# Чтение имён файлов из стандартного ввода
file_names = sys.stdin.read().strip().split()

all_numbers = []
file_contents = {}

# Чтение чисел из файлов
for file_name in sorted(file_names):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            numbers = []
            for line in lines:
                numbers_in_line = list(map(int, line.strip().split()))
                numbers.extend(numbers_in_line)
            file_contents[file_name] = numbers
            all_numbers.extend(numbers)
    except FileNotFoundError:
        print(f"Файл {file_name} не найден. Пропуск...")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}: {e}")

# Вычисление медианы
median = statistics.median(all_numbers) if all_numbers else None

# Фильтрация чисел по медиане
result_lines = []
if median is not None:
    for numbers in file_contents.values():
        filtered_numbers = [str(num) for num in numbers if num < median]
        result_lines.append(' '.join(filtered_numbers))
else:
    result_lines = [''] * len(file_contents)

# Запись результата в файл
with open('face.txt', 'w', encoding='utf-8') as output_file:
    for line in result_lines:
        output_file.write(line + '\n')
