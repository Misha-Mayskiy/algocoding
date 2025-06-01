import re, sys

s = sys.stdin.read()
best = '0'
for seg in re.findall(r'[0-9A-D]+', s):
    for i, ch in enumerate(seg):
        if ch in '02468AC':
            t = seg[:i + 1].lstrip('0') or '0'
            if len(t) > len(best) or (len(t) == len(best) and t > best):
                best = t
print(len(best))
