def solve(n, a):
    # Сортировка длин полосок в порядке убывания
    a.sort(reverse=True)

    # Итерация по отсортированному массиву и разделение полосок на две части
    horizontal = []
    vertical = []
    for i in range(n):
        if i % 2 == 0:
            horizontal.append(a[i])
        else:
            vertical.append(a[i])

    # Вычисление максимальной длины и ширины для каждой части
    max_width = min(len(horizontal), len(vertical))

    # Учет разной длины полосок
    max_area = 0
    for i in range(1, max_width + 1):
        for j in range(i, max_width + 1):
            total_length = 0
            min_length = float('inf')
            for k in range(i):
                total_length += min(horizontal[k], vertical[k])
                min_length = min(min_length, min(horizontal[k], vertical[k]))
            max_length = min(total_length // i, min_length)
            area = max_length * i
            max_area = max(max_area, area)

    return max_area


# Ввод данных
n = int(input())
a = list(map(int, input().split()))

# Вызов функции и вывод результата
print(solve(n, a))
