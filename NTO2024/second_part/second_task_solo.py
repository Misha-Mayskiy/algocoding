def main():
    import sys
    import threading
    sys.setrecursionlimit(1 << 25)
    def solve():
        t = int(sys.stdin.readline())
        for _ in range(t):
            n, m1, m2 = map(int, sys.stdin.readline().split())
            n += 1  # To make indexing from 1
            adj1 = [[] for _ in range(n)]
            adj2 = [[] for _ in range(n)]
            edges1 = set()
            edges2 = set()
            for _ in range(m1):
                u, v = map(int, sys.stdin.readline().split())
                adj1[u].append(v)
                adj1[v].append(u)
                edges1.add((min(u, v), max(u, v)))
            for _ in range(m2):
                u, v = map(int, sys.stdin.readline().split())
                adj2[u].append(v)
                adj2[v].append(u)
                edges2.add((min(u, v), max(u, v)))

            n -= 1  # Adjust back to proper n

            # Find connected components of G1
            parent1 = [i for i in range(n+1)]
            def find(u):
                while parent1[u] != u:
                    parent1[u] = parent1[parent1[u]]
                    u = parent1[u]
                return u
            def union(u, v):
                pu, pv = find(u), find(v)
                if pu != pv:
                    parent1[pu] = pv

            visited1 = [False] * (n +1)
            def dfs1(u):
                visited1[u] = True
                for v in adj1[u]:
                    if not visited1[v]:
                        union(u, v)
                        dfs1(v)
            for u in range(1, n+1):
                if not visited1[u]:
                    dfs1(u)

            # Compute bridges in G2
            bridges = set()
            tin = [0]*(n+1)
            low = [0]*(n+1)
            visited2 = [False]*(n+1)
            timer = [1]
            def dfs2(u, p):
                visited2[u] = True
                tin[u] = low[u] = timer[0]
                timer[0] +=1
                for v in adj2[u]:
                    if v == p:
                        continue
                    if visited2[v]:
                        low[u] = min(low[u], tin[v])
                    else:
                        dfs2(v, u)
                        low[u] = min(low[u], low[v])
                        if low[v] > tin[u]:
                            bridges.add((min(u,v), max(u,v)))
            dfs2(1, -1)

            # Now, try to connect components of G1 without disconnecting G2
            representatives = {}
            for u in range(1, n+1):
                pu = find(u)
                if pu not in representatives:
                    representatives[pu] = u
            comps = list(representatives.keys())
            k = len(comps)
            if k ==1:
                print("Yes")
                print(0)
                continue
            operations = []
            component_vertices = {}
            for u in range(1, n+1):
                pu = find(u)
                component_vertices.setdefault(pu, []).append(u)
            # Build adjacency set for G2
            adj_set2 = [{} for _ in range(n+1)]
            for u in range(1, n+1):
                for v in adj2[u]:
                    adj_set2[u][v] = True

            # Build set of bridges for quick lookup
            bridge_set = set(bridges)
            success = True
            first_comp = comps[0]
            for i in range(1,len(comps)):
                comp = comps[i]
                connected = False
                for u in component_vertices[comp]:
                    for v in component_vertices[first_comp]:
                        edge = (min(u,v), max(u,v))
                        if edge in edges2:
                            if edge in bridge_set:
                                continue
                            else:
                                # Edge exists in G2 and not a bridge
                                operations.append((u,v))
                                union(u,v)
                                connected=True
                                break
                        else:
                            # Edge does not exist in G2
                            operations.append((u,v))
                            union(u,v)
                            connected=True
                            break
                    if connected:
                        break
                if not connected:
                    success = False
                    break
            if success:
                print("Yes")
                print(len(operations))
                for u,v in operations:
                    print(u,v)
            else:
                print("No")
    threading.Thread(target=solve).start()
main()