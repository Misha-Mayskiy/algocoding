import sys

sys.setrecursionlimit(10 ** 6)
t, deps = {}, {}
for line in sys.stdin:
    if line.strip():
        pid, tm, d = line.split(maxsplit=2)
        pid, tm = int(pid), int(tm)
        t[pid] = tm
        deps[pid] = [] if d.strip() == '0' else list(map(int, d.split(';')))

memo = {}
def dfs(p):
    if p not in memo:
        memo[p] = t[p] + (0 if not deps[p] else max(dfs(q) for q in deps[p]))
    return memo[p]

print(max(dfs(p) for p in t))
