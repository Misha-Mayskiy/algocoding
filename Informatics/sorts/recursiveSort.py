# def recursive_sort(lst, idx=0):
#     if idx == len(lst):
#         return lst
#
#     min_idx = idx
#     for i in range(idx + 1, len(lst)):
#         if lst[i] < lst[min_idx]:
#             min_idx = i
#     lst[idx], lst[min_idx] = lst[min_idx], lst[idx]
#
#     return recursive_sort(lst, idx + 1)
#
# print(recursive_sort([int(x) for x in input().split(',')]))

def select_sort(lst):
    for i in range(len(lst)):
        min_idx = i
        for j in range(i + 1, len(lst)):
            if lst[j] < lst[min_idx]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
    return lst


print(select_sort([float(x) for x in input().split(',')]))
