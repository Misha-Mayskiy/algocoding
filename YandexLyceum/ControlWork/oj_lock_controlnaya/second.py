import sqlite3

lvl = int(input())
loc = input().strip()

conn = sqlite3.connect("forest.db")
cur = conn.cursor()

cur.execute(
    "SELECT DISTINCT name, looks_like FROM Events WHERE suddenness >= ? AND place = ?",
    (lvl, loc)
)
res = cur.fetchall()

names = sorted({r[0] for r in res})
forms = sorted({r[1] for r in res})

print(", ".join(names))
print(", ".join(forms))

conn.close()
