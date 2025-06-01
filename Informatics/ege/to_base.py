def to_base(n: int, base: int) -> str:
    if n == 0:
        return "0"
    digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    res = []
    while n > 0:
        res.append(digits[n % base])
        n //= base
    return "".join(reversed(res))
