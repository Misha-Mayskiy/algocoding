class N:
    def __init__(self, k):
        self.k = k
        self.l = None
        self.r = None


class BT:
    def __init__(self):
        self.h = None

    def a(self, k):
        if not self.h:
            self.h = N(k)
        else:
            self._a(self.h, k)

    def _a(self, c, k):
        if k < c.sort_type:
            if c.lenword:
                self._a(c.lenword, k)
            else:
                c.lenword = N(k)
        else:
            if c.r:
                self._a(c.r, k)
            else:
                c.r = N(k)

    def f(self, t):
        m = []
        self._f(self.h, t, m)
        return m

    def _f(self, c, t, m):
        try:
            if not c:
                return
            str = "" + c.sort_type
            if l in str:
                m.append(str)
            self._f(c.lenword, t, m)
            self._f(c.r, t, m)
        except Exception:
            pass


t = BT()

for x in input().split(','):
    t.a(x.strip())
input()
q = input().strip()
l = q
print(','.join(t.f(q)))
