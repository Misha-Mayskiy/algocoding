def longest_increasing_path(matrix: list) -> int:
    """
    Находит длину самой длинной нарастающей последовательности в матрице.

    Параметры:
    matrix (list of list of int): Матрица целых чисел.

    Возвращает:
    int: Длина самой длинной нарастающей последовательности.
    """
    # Если матрица пустая, возвращаем 0
    if not matrix:
        return 0

    # Определяем количество строк и столбцов в матрице
    rows = len(matrix)
    cols = len(matrix[0])

    # Создаем матрицу dp для хранения длин нарастающих последовательностей
    dp = [[0] * cols for _ in range(rows)]
    max_length = 0

    def dfs(i, j):
        # Если значение уже вычислено, возвращаем его
        if dp[i][j] != 0:
            return dp[i][j]

        # Определяем возможные направления движения (вправо, влево, вниз, вверх)
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        current_max = 1

        # Проходим по всем возможным направлениям
        for dx, dy in directions:
            x, y = i + dx, j + dy
            # Проверяем, находится ли новая ячейка в пределах матрицы и является ли она больше текущей
            if 0 <= x < rows and 0 <= y < cols and matrix[x][y] > matrix[i][j]:
                current_max = max(current_max, 1 + dfs(x, y))

        # Сохраняем длину последовательности в dp и возвращаем её
        dp[i][j] = current_max
        return current_max

    # Проходим по всем ячейкам матрицы
    for i in range(rows):
        for j in range(cols):
            # Если значение в dp ещё не вычислено, вызываем dfs
            if dp[i][j] == 0:
                dfs(i, j)
            # Обновляем максимальную длину последовательности
            max_length = max(max_length, dp[i][j])

    # Возвращаем максимальную длину последовательности
    return max_length


# # Примеры использования
# matrix1 = [
#     [9, 9, 4],
#     [6, 6, 8],
#     [2, 1, 1]
# ]
# # 1 -> 2 -> 6 -> 9
# print(longest_increasing_path(matrix1))  # Выход: 4
#
# matrix2 = [
#     [3, 4, 5],
#     [3, 2, 6],
#     [2, 2, 1]
# ]
# # 2 -> 4 -> 5 -> 6
# print(longest_increasing_path(matrix2))  # Выход: 4

matrix1 = [
    [1, 2, 4, 5],
    [0, 0, 1, 5],
    [0, 3, 4, 8],
    [1, 6, 5, 6],
    [8, 7, 3, 5]
]
# 1 -> 2 -> 6 -> 9
print(longest_increasing_path(matrix1))
