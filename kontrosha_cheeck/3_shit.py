def simple_dimple(i):
    for k in range(2, int(i ** 0.5 + 10)):
        l = 2
        while k ** l <= i:
            if k ** l == i:
                return True
            l += 1
    return False


N = 10 ** 10


def dividers(N):
    D = []
    d = 2
    while d * d <= N:
        if N % d == 0:
            D = D + [d]
            d_new = N // d
            if d_new != d:
                D = D + [d_new]
        d += 1
    D += [N]
    D.sort()

    return D

m = dividers(N)
print(len(m), m)
bad_divs = []
for i in m:
    if simple_dimple(i):
        bad_divs.append(i)
print(len(bad_divs), bad_divs)
