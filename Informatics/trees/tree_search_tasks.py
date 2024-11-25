import re


class ZN:
    def __init__(self, nm, ps):
        self.nm = nm
        self.ps = ps
        self.lv = 1
        self.lt = None
        self.rt = None


class ZTree:
    def add_z(self, rt, nm, p):
        if not rt:
            return ZN(nm, [p])
        if nm < rt.nm:
            rt.lt = self.add_z(rt.lt, nm, p)
        elif nm > rt.nm:
            rt.rt = self.add_z(rt.rt, nm, p)
        else:
            rt.ps.append(p)
            return rt
        rt.lv = 1 + max(self.h(rt.lt), self.h(rt.rt))
        b = self.b(rt)
        if b > 1:
            if nm < rt.lt.nm:
                return self.r_r(rt)
            if nm > rt.lt.nm:
                rt.lt = self.r_l(rt.lt)
                return self.r_r(rt)
        if b < -1:
            if nm > rt.rt.nm:
                return self.r_l(rt)
            if nm < rt.rt.nm:
                rt.rt = self.r_r(rt.rt)
                return self.r_l(rt)
        return rt

    def rm_z(self, rt, nm):
        if not rt:
            return rt
        if nm < rt.nm:
            rt.lt = self.rm_z(rt.lt, nm)
        elif nm > rt.nm:
            rt.rt = self.rm_z(rt.rt, nm)
        else:
            if not rt.lt:
                return rt.rt
            if not rt.rt:
                return rt.lt
            t = self.min(rt.rt)
            rt.nm = t.nm
            rt.ps = t.ps
            rt.rt = self.rm_z(rt.rt, t.nm)
        rt.lv = 1 + max(self.h(rt.lt), self.h(rt.rt))
        b = self.b(rt)
        if b > 1:
            if self.b(rt.lt) >= 0:
                return self.r_r(rt)
            rt.lt = self.r_l(rt.lt)
            return self.r_r(rt)
        if b < -1:
            if self.b(rt.rt) <= 0:
                return self.r_l(rt)
            rt.rt = self.r_r(rt.rt)
            return self.r_l(rt)
        return rt

    def srch_z(self, rt, nm):
        if not rt:
            return []
        if nm == rt.nm:
            return rt.ps
        if nm < rt.nm:
            return self.srch_z(rt.lt, nm)
        return self.srch_z(rt.rt, nm)

    def min(self, n):
        while n.lt:
            n = n.lt
        return n

    def h(self, n):
        return n.lv if n else 0

    def b(self, n):
        return self.h(n.lt) - self.h(n.rt)

    def r_l(self, n):
        y = n.rt
        t = y.lt
        y.lt = n
        n.rt = t
        n.lv = 1 + max(self.h(n.lt), self.h(n.rt))
        y.lv = 1 + max(self.h(y.lt), self.h(y.rt))
        return y

    def r_r(self, n):
        y = n.lt
        t = y.rt
        y.rt = n
        n.lt = t
        n.lv = 1 + max(self.h(n.lt), self.h(n.rt))
        y.lv = 1 + max(self.h(y.lt), self.h(y.rt))
        return y


def ex_d(t):
    return [(m.group(), m.start()) for m in re.finditer(r'\b\w+\b', t)]


def gp(w, t):
    return [m.start() for m in re.finditer(r'\b' + re.escape(w) + r'\b', t)]


d = input().strip()
input()
e = input().strip()
input()
x = set(w for w, _ in ex_d(e))
p = d
for w in x:
    p = re.sub(r'\b' + re.escape(w) + r'\b', '', p, flags=re.IGNORECASE)
s = input().strip().lower()
o = gp(s, p)
print(",".join(map(str, o)))
