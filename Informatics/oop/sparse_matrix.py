import sys

def max_path(m):
    n = len(m)
    max_val = -1
    dict_vis = set()

    def dfs(i, cur):
        nonlocal max_val
        if len(dict_vis) == n:
            max_val = max(max_val, cur)
            return

        for j in range(n):
            if j not in dict_vis and m[i][j] != 0:
                dict_vis.add(j)
                dfs(j, cur * m[i][j])
                dict_vis.remove(j)

    for i in range(n):
        dict_vis.add(i)
        dfs(i, 1)
        dict_vis.remove(i)

    return max_val > 0

m = [list(map(int, line.split())) for line in sys.stdin]
print(str(max_path(m)).lower())
