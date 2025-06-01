memo = {}
def dp(x, seen14):
    if (x, seen14) in memo:
        return memo[(x, seen14)]
    if x == 18:
        return 1 if seen14 else 0
    total = 0
    for y in (x + 1, x + 2, x * 2):
        if y <= 18 and y != 8:
            total += dp(y, seen14 or y == 14)
    memo[(x, seen14)] = total
    return total


print(dp(3, False))
