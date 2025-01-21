def max_sequence(nums):
    # Если список пустой, то последовательность = 0
    if not nums:
        return 0

    # Конвертируем список во множество
    num_set = set(nums)
    max_streak_counter = 0

    for num in nums:

        # Проверка является ли число началом последовательности
        if num - 1 not in num_set:
            cur_num = num
            cur_streak_counter = 1

            # Находим длину последовательности пока следующее число в
            while cur_num + 1 in num_set:
                cur_num += 1
                cur_streak_counter += 1

            # Обновляем максимальную длину последовательности
            max_streak_counter = max(max_streak_counter, cur_streak_counter)

    # Возвращаем максимальную последовательность
    return max_streak_counter


print(max_sequence([100, 4, 200, 1, 3, 2]))
print(max_sequence([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))
