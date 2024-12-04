# import sys
#
# def to_coordinate_format(matrix):
#     values, col_indices, row_indices = [], [], []
#     for i, row in enumerate(matrix):
#         for j, value in enumerate(row):
#             if value != 0:
#                 values.append(value)
#                 col_indices.append(j)
#                 row_indices.append(i)
#     return values, col_indices, row_indices
#
# matrix = [list(map(int, line.split())) for line in sys.stdin if line.strip()]
# values, col_indices, row_indices = to_coordinate_format(matrix)
#
# print(" ".join(map(str, values)))
# print(" ".join(map(str, col_indices)))
# print(" ".join(map(str, row_indices)))

# import sys
#
# def sparse_matrix_vector_multiply(values, col_indices, row_indices, vector, rows):
#     result = [0] * rows
#     for v, c, r in zip(values, col_indices, row_indices):
#         result[r] += v * vector[c]
#     return result
#
# data = [list(map(int, line.split())) for line in sys.stdin if line.strip()]
# values, col_indices, row_indices, vector = data[0], data[1], data[2], data[3:]
# rows = max(row_indices) + 1
# result = sparse_matrix_vector_multiply(values, col_indices, row_indices, [v[0] for v in vector], rows)
#
# print("\n".join(map(str, result)))

# import sys
#
# def to_csr(matrix):
#     values, column_indices, row_pointer = [], [], [0]
#     for row in matrix:
#         for col_index, value in enumerate(row):
#             if value != 0:
#                 values.append(value)
#                 column_indices.append(col_index)
#         row_pointer.append(len(values))
#     return values, column_indices, row_pointer
#
# input_matrix = [list(map(int, line.split())) for line in sys.stdin if line.strip()]
# values, column_indices, row_pointer = to_csr(input_matrix)
# print(*values)
# print(*column_indices)
# print(*row_pointer)

import sys

data = [list(map(int, line.split())) for line in sys.stdin if line.strip()]
values, col_indices, row_ptr, vector = data[0], data[1], data[2], [x[0] for x in data[3:]]
result = []
for i in range(len(row_ptr) - 1):
    row_start, row_end = row_ptr[i], row_ptr[i + 1]
    row_sum = sum(values[j] * vector[col_indices[j]] for j in range(row_start, row_end))
    result.append(row_sum)
print("\n".join(map(str, result)))
