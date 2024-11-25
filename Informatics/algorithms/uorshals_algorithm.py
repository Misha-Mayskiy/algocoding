def transitive_closure():
    g = []
    while True:
        try:
            g.append(list(map(int, input().split())))
        except EOFError:
            break

    n = len(g)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                g[i][j] = g[i][j] or (g[i][k] and g[k][j])

    for row in g:
        print(" ".join(map(str, row)))

transitive_closure()
