class N:
    def __init__(self):
        self.c = {}
        self.v = None


class T:
    def __init__(self):
        self.r = N()

    def a(self, k, v):
        cur = self.r
        for ch in k:
            if ch not in cur.c:
                cur.c[ch] = N()
            cur = cur.c[ch]
        cur.v = v

    def f(self, k):
        cur = self.r
        for ch in k:
            if ch not in cur.c:
                return None
            cur = cur.c[ch]
        return cur.v


t = T()

while True:
    l = input()
    if l == "":
        break
    k, v = l.split(" - ")
    t.a(k, v)

k = input()
res = t.f(k)

if res:
    print(res)
else:
    print("нет")
