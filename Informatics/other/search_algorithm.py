from collections import defaultdict

def find_similar_strings(input_strings):
    groups = defaultdict(list)

    # Группировка строк по набору символов
    for s in input_strings:
        key = frozenset(s)
        groups[key].append(s)

    # Отфильтруем группы с менее чем 2 строками
    filtered_groups = [group for group in groups.values() if len(group) >= 2]

    # Сортировка групп по числу строк, затем по общей длине
    filtered_groups.sort(key=lambda g: (-len(g), -sum(len(s) for s in g)))

    # Вывод результата
    result = ["\n".join(",".join(group) for group in filtered_groups)]
    return result


# Пример ввода
input_strings = input().split(",")
output = find_similar_strings(input_strings)

# Вывод результата
print("\n\n".join(output))
