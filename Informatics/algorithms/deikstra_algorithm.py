import heapq

a, b, c = map(int, input().split())
b -= 1
c -= 1

g = []
for _ in range(a):
    g.append(list(map(int, input().split())))

d = [float('inf')] * a
d[b] = 0
q = [(0, b)]

while q:
    cd, u = heapq.heappop(q)
    if cd > d[u]:
        continue
    for v in range(a):
        if g[u][v] != -1 and u != v:
            nd = cd + g[u][v]
            if nd < d[v]:
                d[v] = nd
                heapq.heappush(q, (nd, v))

print(d[c] if d[c] != float('inf') else -1)
