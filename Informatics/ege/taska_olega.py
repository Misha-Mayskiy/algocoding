def min_del(number):
    for i in range(2, int(number ** 0.5) + 1):
        if not number % i:
            return i
    return 0


def max_del(number):
    for i in range(number // 2 + 1, 2, -1):
        if not number % i:
            return i
    return 0


i = 700000
finded = 0
str_ans = ""
while finded != 5:
    max_delitel = max_del(i)
    min_delitel = min_del(i)
    M = max_delitel + min_delitel
    if M % 10 == 8:
        finded += 1
        str_ans += f"{i} {M}\n"
    i += 1

print(str_ans)
