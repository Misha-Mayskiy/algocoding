import statistics
import sys

# Чтение имён файлов из стандартного ввода
file_names = sys.stdin.read().strip().split()

all_numbers = []
result_lines = []

# Чтение чисел из файлов
for file_name in sorted(file_names):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for line in lines:
                numbers_in_line = list(map(int, line.strip().split()))
                result_lines.append(numbers_in_line)  # Сохраняем каждую строку
                all_numbers.extend(numbers_in_line)  # Собираем все числа для медианы

    except FileNotFoundError:
        print(f"Файл {file_name} не найден. Пропуск...")
    except Exception as e:
        print(f"Ошибка при чтении файла {file_name}: {e}")

# Вычисление медианы
median = statistics.median(all_numbers) if all_numbers else None

# Фильтрация чисел по медиане и запись результата
with open('face.txt', 'w', encoding='utf-8') as output_file:
    for numbers in result_lines:
        filtered_numbers = [str(num) for num in numbers if num < median]
        output_file.write(' '.join(filtered_numbers) + '\n')
