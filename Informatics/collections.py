# def input_matrix():
#     size = input()
#     rows, cols = map(int, size.split('x'))
#     matrix = [list(map(int, input().split())) for _ in range(rows)]
#     return matrix
#
# matrix1 = input_matrix()
# matrix2 = input_matrix()
#
# rows1, cols1 = len(matrix1), len(matrix1[0]) if matrix1 else 0
# rows2, cols2 = len(matrix2), len(matrix2[0]) if matrix2 else 0
#
# result_rows = max(rows1, rows2)
# result_cols = max(cols1, cols2)
#
# result_matrix = [[0] * result_cols for _ in range(result_rows)]
#
# for i in range(result_rows):
#     for j in range(result_cols):
#         val1 = matrix1[i][j] if i < rows1 and j < cols1 else 0
#         val2 = matrix2[i][j] if i < rows2 and j < cols2 else 0
#         result_matrix[i][j] = val1 + val2
#
# print(result_matrix)

# n, m = map(int, input().split())
# matrix = [[0] * m for _ in range(n)]
# num = 1
#
# for diag in range(n + m - 1):
#     row, col = (0, diag) if diag < m else (diag - m + 1, m - 1)
#     while row < n and col >= 0:
#         matrix[row][col] = num
#         num += 1
#         row += 1
#         col -= 1
#
# max_len = len(str(num - 1))
# for row in matrix:
#     print(*[f"{x:<{max_len}}" for x in row])

# row, n = [1], int(input())
# for k in range(1, n + 1):
#     row.append(row[-1] * (n - k + 1) // k)
# print(row)

# numbers = list(map(int, input().split()))
# print(len(tuple(num for num in numbers if num > 0)),
#       len(tuple(num for num in numbers if num < 0)))

# numbers = tuple(map(float, input().split()))
# print(max(numbers), min(numbers), sum(numbers))

# print(tuple(sorted(eval(input()), key=lambda x: x[2])))
