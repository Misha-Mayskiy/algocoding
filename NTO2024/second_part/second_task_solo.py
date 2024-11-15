from collections import defaultdict


def searching_moment(secretx):
    while secretx != parens[secretx]:
        parens[secretx] = parens[parens[secretx]]
        secretx = parens[secretx]
    return secretx


def unioning_moment(secretx, needy):
    root_of_iksoid, root_of_igroid = searching_moment(secretx), searching_moment(needy)
    if root_of_iksoid != root_of_igroid:
        parens[root_of_iksoid] = root_of_igroid
        return True
    return False


t = int(input())
for _ in range(t):
    nodiki_kol, edgesiki_kol_first, edgesiki_kol_second = map(int, input().split())
    edgesiki_f, adjl = set(), [set() for _ in range(nodiki_kol)]
    for _ in range(edgesiki_kol_first):
        a, b = sorted(map(lambda x: int(x) - 1, input().split()))
        edgesiki_f.add((a, b))
    for _ in range(edgesiki_kol_second):
        a, b = map(lambda x: int(x) - 1, input().split())
        adjl[a].add(b)
        adjl[b].add(a)
    if edgesiki_kol_second == nodiki_kol * (nodiki_kol - 1) // 2:
        print('No')
        continue
    print('Yes')
    parens = list(range(nodiki_kol))
    for a, b in edgesiki_f:
        unioning_moment(a, b)
    groupki = defaultdict(set)
    for i in range(nodiki_kol):
        groupki[searching_moment(i)].add(i)
    oreps = []
    compounds = list(groupki.values())
    for i in range(len(compounds) - 1):
        x, y = next(iter(compounds[i])), next(iter(compounds[i + 1]))
        if (min(x, y), max(x, y)) not in edgesiki_f:
            oreps.append((x + 1, y + 1))
            unioning_moment(x, y)
    print(len(oreps))
    for a, b in oreps:
        print(a, b)
