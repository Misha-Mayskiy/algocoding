# string = input()
# if string.count("[") != string.count("]"):
#     print("Incorrect input string")
#     exit()
#
# string = string[string.index("[")::]
# wasPoint = False
# stringNew = ""
# for i in string:
#     if wasPoint and i != " ":
#         stringNew += " " + i
#         wasPoint = False
#         continue
#     if i == ",":
#         wasPoint = True
#     stringNew += i
# print(stringNew)


# import random
#
#
# def quicksort(nums):
#     if len(nums) <= 1:
#         return nums
#     else:
#         q = random.choice(nums)
#     l_nums = [n for n in nums if n < q]
#
#     e_nums = [q] * nums.count(q)
#     b_nums = [n for n in nums if n > q]
#     return quicksort(l_nums) + e_nums + quicksort(b_nums)
#
#
# print(quicksort(list(map(int, input().split(",")))))


# I
# m, string = [], input()
# for i in string:
#     try:
#         int(i)
#     except ValueError or TypeError:
#         continue
#     m.append(int(i))
# print(m)

# II
# Рекурсивный метод распаковки списка
# def flatten(lst):
#     result = []
#     if isinstance(lst, list):
#         for sub_item in lst:
#             result.extend(flatten(sub_item))
#     else:
#         result.append(lst)
#     return result

# import ast
# print(flatten(ast.literal_eval(input()))[::-1])
#
#
# def find_min_cover_set(universe, subsets):
#     elements_to_cover, selected_subsets = set(universe), []
#     while elements_to_cover:
#         best_subset = max(subsets, key=lambda s: len(elements_to_cover & set(s)))
#         selected_subsets.append(best_subset)
#         elements_to_cover -= set(best_subset)
#     return selected_subsets


# # universe = eval(input())
# # subsets = eval(input())
# universe, subsets = {1, 2, 3, 4, 5}, [{1, 2, 3}, {2, 4}, {3, 4}, {4, 5}]
# print(universe, subsets, sep="\n")
# print(find_min_cover_set(universe, subsets))
