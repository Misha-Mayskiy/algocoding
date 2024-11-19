# Пользователь вводит строки с клавиатуры.
# Трубется найти все строки в которых совпадает больше трех символов и вывести их в порядке убывания числа совпадений.
# Группы строк с одинаковом количеством совпадений отсортировать в соответствии с количеством входящих в группу символов всех строк.
# Строки, в которых совпадений менбше двух не выводить.
# Алгоритм поиска не должен превосходить по сложности O(N logN)
# Ввод:
# asdf,farta,dasdf,dfasdf23,sdfartd, far
# Вывод:
# asdf,dasdf,dfasdf23
# farta,sdfartd
# farta,far

from collections import defaultdict


def count_common_chars(s1, s2):
    return len(set(s1) & set(s2))


def group_strings(strings):
    groups = defaultdict(list)
    print(groups)

    for i in range(len(strings)):
        for j in range(i + 1, len(strings)):
            common_count = count_common_chars(strings[i], strings[j])
            if common_count >= 2:
                groups[(common_count, len(strings[i]) + len(strings[j]))].append((strings[i], strings[j]))

    sorted_groups = sorted(groups.items(), key=lambda x: (-x[0][0], -x[0][1]))

    result = []
    for _, pairs in sorted_groups:
        for s1, s2 in pairs:
            if s1 not in result:
                result.append(s1)
            if s2 not in result:
                result.append(s2)
    return result


print(','.join(group_strings(input().strip().split(','))))
