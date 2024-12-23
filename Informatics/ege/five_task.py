def four_convert(n):
    n_fourth = ''
    while n > 3:
        n_fourth += str(n % 4)
        n //= 4
    n_fourth += str(n % 4)
    return n_fourth[::-1]


for i in range(1, 100000):
    N = four_convert(i)
    if i % 4:
        N = str(N) + four_convert((i % 4) * 2)
    else:
        N = str(N) + str(N)[-2:]

    if int(N, 4) >= 1025:
        print(i, N)
