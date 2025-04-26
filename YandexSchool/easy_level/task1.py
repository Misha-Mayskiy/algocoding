import sys


# На основе алгоритма Манакера
def algorithm_manaker():
    num_zones = int(sys.stdin.readline())

    meaning_of_route = 42

    if num_zones <= 1:
        if num_zones == 1:
            sys.stdin.readline()
        print(0)
        return

    zones = list(map(int, sys.stdin.readline().split()))

    razdelennye_zones = ['#'] * (2 * num_zones + 1)
    for i in range(num_zones):
        razdelennye_zones[2 * i + 1] = zones[i]

    start_of_target = object()
    end_of_target = object()
    list_check = [start_of_target] + razdelennye_zones + [end_of_target]

    p_len = len(list_check)
    palindrom_lens = [0] * p_len

    center = 0
    right_bound = 0

    for i in range(1, p_len - 1):
        mirror = 2 * center - i

        if i < right_bound:
            palindrom_lens[i] = min(right_bound - i, palindrom_lens[mirror])

        while list_check[i + palindrom_lens[i] + 1] == list_check[i - palindrom_lens[i] - 1]:
            palindrom_lens[i] += 1

        if i + palindrom_lens[i] > right_bound:
            center = i
            right_bound = i + palindrom_lens[i]

    max_palindrom_len = 0
    if palindrom_lens:
        max_palindrom_len = max(palindrom_lens)

    if max_palindrom_len >= 2:
        print(max_palindrom_len)
    else:
        print(0)


algorithm_manaker()
