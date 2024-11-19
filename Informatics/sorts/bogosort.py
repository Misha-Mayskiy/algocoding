import random


def is_sorted(data: list) -> list:
    """Проверяет, отсортирован ли массив"""
    for i in range(len(data) - 1):
        if data[i] > data[i + 1]:
            return False
    return True


def bogosort(data: list) -> list:
    """Сортирует массив с помощью bogosort"""
    while not is_sorted(data):
        random.shuffle(data)
    return data


def bogosort_v2(arr):
    while not all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1)):
        random.shuffle(arr)
    return arr


# Тестирование bogosort
lst = list(range(10))
random.shuffle(lst)
print("Оригинальный массив:", lst)
print("Отсортированный массив:", bogosort_v2(lst))
