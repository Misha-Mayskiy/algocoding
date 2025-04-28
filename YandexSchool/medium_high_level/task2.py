import sys


def index_of_syrok():
    price_counts = [0] * 201

    n = int(sys.stdin.readline())
    if n <= 1:
        return 0

    count_variants = 0

    for _ in range(n):
        now_price = int(sys.stdin.readline())

        count_of_money_talks_days = 0
        for low_price in range(1, now_price):
            count_of_money_talks_days += price_counts[low_price]

        count_variants += count_of_money_talks_days

        price_counts[now_price] += 1

    return count_variants


print(index_of_syrok())
