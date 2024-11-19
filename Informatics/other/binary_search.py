# def min_time_to_copy(N, x, y):
#     if N == 1:
#         return min(x, y)  # Если нужна всего 1 копия, то минимальное время работы одного ксерокса
#
#     # Ищем минимальное время
#     left, right = 0, min(x, y) + (N - 1) * max(x, y)
#
#     while left < right:
#         mid = (left + right) // 2
#         # Считаем количество копий, которые можно сделать за `mid` секунд
#         copies = (mid // x) + (mid // y)
#         if copies >= N - 1:  # +1 копия уже сделана на первом шаге
#             right = mid
#         else:
#             left = mid + 1
#
#     return left + min(x, y)
#
#
# # Чтение входных данных
# with open('INPUT.TXT', 'r') as infile:
#     N, x, y = map(int, infile.read().split())
#
# # Вычисляем минимальное время
# result = min_time_to_copy(N, x, y)
#
# # Запись результата
# with open('OUTPUT.TXT', 'w') as outfile:
#     outfile.write(str(result))

# m = list(map(int, input().split(",")))
# num = int(input())
#
# l, r = 0, len(m)
# while m[l] != num:
#     if num in m[l:r // 2 + 1]:
#         l, r = l, r // 2 + 1
#     else:
#         l, r = r // 2 + 1, r
# print(l)
