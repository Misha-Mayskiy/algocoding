# def sum_divisors(num):
#     if is_simple(num):
#         return num + 1
#     sum_div = 0
#     for i in range(1, num + 1):
#         if num % i == 0:
#             sum_div += i
#     return sum_div
#
#
# count = 0
# for i in range(int(input()), int(input()) + 1):
#     sum_div_i = sum_divisors(i)
#     if is_simple(sum_div_i):
#         print(i, sum_div_i)
#         count += 1
# print(count)
#
#
# cashe = dict()
#
#
# def is_simple(num: int):
#     try:
#         return cashe[num]
#     except:
#         if num <= 1:
#             cashe[num] = False
#             return False
#         for i in range(2, int(num ** 0.5) + 1):
#             if num % i == 0:
#                 cashe[num] = False
#                 return False
#
#         cashe[num] = True
#         return True
#
# count = 0
# print(max([count := count + 1 if is_simple(int(input())) else count for _ in range(int(input()))]))
#
# print("w x y z")
# for w in range(0, 2):
#     for x in range(0, 2):
#         for y in range(0, 2):
#             for z in range(0, 2):
#                 if not (not (not x or z) or (y == w) or y):
#                     print(w, x, y, z)
#
#
# n = 3 * 3125 ** 8 + 2 * 625 ** 7 - 4 * 625 ** 6 + 3 * 125 ** 5 - 2 * 25 ** 4 - 2024
# string = ''
# while n > 0:
#     string += str(n % 25)
#     n //= 25
# print(string[::-1])
#
# n = 2 * 729 ** 333 + 2 * 243 ** 334 - 81 ** 335 + 2 * 27 ** 336 - 2 * 9 ** 337 - 338
# string = ''
# count = 0
# while n > 0:
#     string += str(n % 9)
#     if str(n % 9) != 0:
#         count += 1
#     n //= 9
# print(count)
# print(string[::-1])
#
# for n in range(4, 1001):
#     string = "7" * 15 + "4" * 20 + "5" * n
#     while ("74" in string) or ("75" in string):
#         if "75" in string:
#             string = string.replace("75", "744", 1)
#         else:
#             string = string.replace("74", "44", 1)
#     print(string)
#
# for n in range(4, 1001):
#     string = "5" + "2" * n
#     while ("72" in string) or ("522" in string) or ("2222" in string):
#         if "72" in string:
#             string = string.replace("72", "2", 1)
#         if "522" in string:
#             string = string.replace("522", "27", 1)
#         if "2222" in string:
#             string = string.replace("2222", "5", 1)
#     if sum(list(map(int, " ".join(string).split()))) == 22:
#         print(n)
#
#
# # Чтение данных из файла
# with open('17_1.txt', 'r') as file:
#     numbers = list(map(int, file.readlines()))
#
# # Нахождение минимального элемента последовательности
# min_element = min(numbers)
#
# # Переменные для хранения результата
# count = 0
# max_sum = float('-inf')
#
# # Поиск пар подряд идущих чисел
# for i in range(len(numbers) - 1):
#     a = numbers[i] % 77
#     b = numbers[i + 1] % 77
#     if a + b == min_element:
#         count += 1
#         pair_sum = numbers[i] + numbers[i + 1]
#         if pair_sum > max_sum:
#             max_sum = pair_sum
#
# # Вывод результата
# print(count, max_sum)

