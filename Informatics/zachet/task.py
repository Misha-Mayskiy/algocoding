def max_sequence(nums: list) -> int:
    """
    Находит длину самой длинной последовательности последовательных элементов в несортированном массиве.

    Params:
    nums (list of int): Несортированный массив целых чисел.

    Return:
    int: Длина самой длинной последовательности последовательных элементов.
    """

    # Если список пустой, то последовательность = 0
    if not nums:
        return 0

    num_set = set(nums)
    max_streak_counter = 0

    for num in nums:
        # Проверка является ли число началом последовательности
        if num - 1 not in num_set:
            cur_num = num
            cur_streak_counter = 1

            # Находим длину последовательности пока следующее число в множестве
            while cur_num + 1 in num_set:
                cur_num += 1
                cur_streak_counter += 1

            # Обновляем максимальную длину последовательности
            max_streak_counter = max(max_streak_counter, cur_streak_counter)

    # Возвращаем максимальную последовательность
    return max_streak_counter

# Примеры использования
print(max_sequence([100, 4, 200, 1, 3, 2])) # -> 4
print(max_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1])) # -> 9
