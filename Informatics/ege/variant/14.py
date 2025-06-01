def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    while n > 0:
        res.append(digits[n % base])
        n //= base
    print("".join(reversed(res)))
    return "".join(reversed(res))


def find_max_x(limit, zero_count):
    T = 7 ** 350 + 7 ** 150
    for x in range(limit, 0, -1):
        s7 = to_base(T - x, 7)
        if s7.count('0') == zero_count:
            return x
    return None


ans = find_max_x(limit=2300, zero_count=200)
print("Ответ (десятичное):", ans)
