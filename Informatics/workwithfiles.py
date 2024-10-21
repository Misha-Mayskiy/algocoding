# def read_last(linescount, file):
#     with open(file, "r") as f:
#         lines = f.readlines()
#     print("".join(lines[len(lines)-linescount:]))
#
# n = int(input())
# read_last(n, "file.txt")

# def longest_words(file):
#     with open(file, "r") as f:
#         lines = f.readlines()
#     maxlength = 0
#     m = []
#     for i in lines:
#         for j in i.split():
#             if len(j) > maxlength:
#                 m = [j]
#                 maxlength = len(j)
#             elif len(j) == maxlength:
#                 m.append(j)
#     print(*m)
#
# longest_words("file.txt")

# def longest_words(file):
#     with open(file, "r") as f:
#         lines = f.readlines()
#     words, letters = 0, 0
#     for i in lines:
#         for j in i.split():
#             words += 1
#             for p in j:
#                 if p.lower() in "qwertyuiopasdfghjklzxcvbnm":
#                     letters += 1
#     print("Input file contains:", f"{letters} letters", f"{words} words", f"{len(lines)} lines", sep="\n")
#
# longest_words("data.txt")

# def censor_forbidden_words(data_file):
#     with open('forbidden_words.txt', 'r') as f:
#         forbidden_words = set(word.strip() for word in f.read().split())
#
#     with open(data_file, 'r', encoding='utf-8') as f:
#         content = f.read()
#
#     for word in forbidden_words:
#         content = content.replace(word, '*' * len(word))
#         content = content.replace(word.capitalize(), '*' * len(word))
#         content = content.replace(word.upper(), '*' * len(word))
#         content = content.replace(word.lower(), '*' * len(word))
#         for i in range(len(word)):
#             mixed_case = word[:i] + word[i:].capitalize()
#             content = content.replace(mixed_case, '*' * len(word))
#     print(content)
#
# censor_forbidden_words(input())

def count_fruits(file_name):
    with open(file_name, 'r') as f:
        words = f.read().lower().split()

    fruit_counts = {}
    for word in words:
        fruit_counts[word] = fruit_counts.get(word, 0) + 1

    print("Названия этих фруктов встречаются в тексте:")
    for fruit, count in fruit_counts.items():
        print(f'"{fruit}" - {count} раз(а)')

count_fruits('fruits.txt')

# def check_grades(file_name):
#     with open(file_name, 'r', encoding='utf-8') as f:
#         for line in f:
#             data = line.split()
#             name, grades = ' '.join(data[:-4]), list(map(int, data[-4:]))
#             average = sum(grades) / len(grades)
#             if average >= 4.5:
#                 print(f'{name}, средний балл: {average:.2f}')
#
# check_grades('grades.txt')

# def process_log(log_file, output_file):
#     with open(log_file, 'r') as f:
#         employees = []
#         for line in f:
#             name, entry_time, exit_time = line.strip().split(', ')
#             entry_hour, entry_minute = map(int, entry_time.split(':'))
#             exit_hour, exit_minute = map(int, exit_time.split(':'))
#             duration = (exit_hour * 60 + exit_minute) - (entry_hour * 60 + entry_minute)
#             if duration > 240:  # 4 часа в минутах
#                 employees.append(name)
#
#     with open(output_file, 'w') as f:
#         for employee in employees:
#             f.write(employee + '\n')
#
#     with open(output_file, 'r') as f:
#         print(f.read())
#
# process_log('crm_log.txt', 'best_employees.txt')
