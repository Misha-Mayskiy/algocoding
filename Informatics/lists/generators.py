# def generate_matrix(N):
#     # Создаем пустую матрицу N x N
#     matrix = [[0] * N for _ in range(N)]
#
#     # Заполняем матрицу
#     for i in range(N):
#         for j in range(N):
#             # Определяем минимальное расстояние до углов
#             distance_to_corner = min(i, j, N - 1 - i, N - 1 - j)
#             matrix[i][j] = distance_to_corner
#
#     return matrix
#
#
# def print_matrix(matrix):
#     for row in matrix:
#         print(" ".join(map(str, row)))
#
#
# # Ввод числа N
# N = int(input("Введите целое число N: "))
# result_matrix = generate_matrix(N)
# print_matrix(result_matrix)
from numpy.matrixlib.defmatrix import matrix


# n = int(input())
# sp = [[abs(n - 1 - (j + i)) for j in range(n)] for i in range(n)]
# for row in sp:
#     print(*row)

# n = int(input())
# az = [input().split() for i in range(n)]
# dc = [[az[t][i] for t in range(n - 1, -1, -1)] for i in range(n)]
#
# for i in dc:
#     print(*i)

# n = int(input())
# m = int(input())
#
# print('\n'.join(' '.join(str(i * m + j) for j in range(m)) for i in range(n)))

# def generate_matrix(N):
#     for i in range(N):
#         row = (
#             min(i + j, i + (N - 1 - j), (N - 1 - i) + j, (N - 1 - i) + (N - 1 - j))
#             for j in range(N)
#         )
#         yield row
#
# N = int(input())
# matrix_gen = generate_matrix(N)
# for row in matrix_gen:
#     print(' '.join(map(str, row)))

def generate_magic_square(n):
    """
    Генерация магического квадрата размера n x n.
    Поддерживаются нечетные, двукратно четные и простонечетные порядки.
    Если невозможна генерация, возвращает None.
    """
    if n < 1:
        return None
    elif n == 2:
        return None  # Магический квадрат 2x2 не существует
    elif n % 2 == 1:
        return generate_odd_magic_square(n)
    elif n % 4 == 0:
        return generate_doubly_even_magic_square(n)
    else:
        return generate_singly_even_magic_square(n)


def generate_odd_magic_square(n):
    """
    Генерация магического квадрата нечетного порядка (Siamese method).
    """
    magic_square = [[0 for _ in range(n)] for _ in range(n)]

    num = 1
    i, j = 0, n // 2

    while num <= n * n:
        magic_square[i][j] = num
        num += 1
        newi, newj = (i - 1) % n, (j + 1) % n
        if magic_square[newi][newj]:
            i = (i + 1) % n
        else:
            i, j = newi, newj

    return magic_square


def generate_doubly_even_magic_square(n):
    """
    Генерация магического квадрата двукратно четного порядка.
    """
    magic_square = [[(n * i) + j + 1 for j in range(n)] for i in range(n)]

    for i in range(n):
        for j in range(n):
            if (i % 4 == j % 4) or ((i + j) % 4 == 3):
                magic_square[i][j] = (n * n + 1) - magic_square[i][j]

    return magic_square


def generate_singly_even_magic_square(n):
    half_n = n // 2
    sub_magic = generate_odd_magic_square(half_n)

    magic_square = [[0 for _ in range(n)] for _ in range(n)]
    add = [0, 2 * half_n * half_n, 3 * half_n * half_n, half_n * half_n]

    for i in range(half_n):
        for j in range(half_n):
            val = sub_magic[i][j]
            magic_square[i][j] = val + add[0]
            magic_square[i][j + half_n] = val + add[1]
            magic_square[i + half_n][j] = val + add[2]
            magic_square[i + half_n][j + half_n] = val + add[3]

    k = half_n // 2
    for i in range(n):
        for j in range(n):
            if (j < k or j >= n - k) and i < half_n:
                if j == 0 and i == k:
                    continue
                magic_square[i][j], magic_square[i + half_n][j] = magic_square[i + half_n][j], magic_square[i][j]
    return magic_square


N = int(input())
magic_square = generate_magic_square(N)
for row in magic_square:
    print(' '.join(map(str, row)))
