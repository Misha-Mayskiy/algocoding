MIN_RUN = 32

# Сортировка вставками
def insertion_sort(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key

# Слияние двух подмассивов
def merge(arr, left, mid, right):
    left_part, right_part = arr[left:mid + 1], arr[mid + 1:right + 1]
    i, j, k = 0, 0, left
    while i < len(left_part) and j < len(right_part):
        if left_part[i] <= right_part[j]:
            arr[k] = left_part[i]
            i += 1
        else:
            arr[k] = right_part[j]
            j += 1
        k += 1
    arr[k:k + len(left_part) - i] = left_part[i:]
    arr[k:k + len(right_part) - j] = right_part[j:]

# Основная функция Timsort
def timsort(arr):
    n = len(arr)

    # Сортируем подмассивы с помощью сортировки вставками
    for i in range(0, n, MIN_RUN):
        insertion_sort(arr, i, min(i + MIN_RUN - 1, n - 1))

    # Сливаем подмассивы
    size = MIN_RUN
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(n - 1, left + 2 * size - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2


import random
lst = list(range(999999))
random.shuffle(lst)
random.shuffle(lst)
random.shuffle(lst)
print(lst)
print(lst.sort())
timsort(lst)
print(lst)
