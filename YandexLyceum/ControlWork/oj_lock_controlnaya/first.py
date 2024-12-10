import csv
import sys


def calc_power(krolic, kraza):
    return len(krolic) * (kraza // 2)


data = {}
for line in sys.stdin:
    if not line.strip():
        break
    craft, crolik, craza = line.strip().split("; ")
    craza = int(craza)
    if craft not in data:
        data[craft] = (crolik, craza, calc_power(crolik, craza))

with open("fairytale.csv", "w", newline="", encoding="utf-8") as f:
    wrot = csv.writer(f)
    wrot.writerow(["no", "creature", "habitat", "stealth", "power"])
    wrot.writerows([[i, c, *props] for i, (c, props) in enumerate(data.items(), 1)])
