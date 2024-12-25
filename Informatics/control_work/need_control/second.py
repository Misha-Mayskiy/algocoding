class Graph:
    def __init__(self, stock_matr):
        self.conf_matrix = stock_matr

    def compute_transitive(self):
        c_vert = len(self.conf_matrix)
        ach_matrix = [row[:] for row in self.conf_matrix]  # Копируем матрицу смежности

        for mid_vert in range(c_vert):
            for start_vert in range(c_vert):
                for to_vert in range(c_vert):
                    ach_matrix[start_vert][to_vert] = (
                        ach_matrix[start_vert][to_vert] or
                        (ach_matrix[start_vert][mid_vert] and
                         ach_matrix[mid_vert][to_vert])
                    )

        return ach_matrix

if __name__ == "__main__":
    import sys

    matrix = [list(map(int, line.split())) for line in sys.stdin]

    graph = Graph(matrix)
    ans_matrix = graph.compute_transitive()

    for row in ans_matrix:
        print(" ".join(map(str, row)))
