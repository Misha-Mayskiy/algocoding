import csv
import sys

m = []
file = open("plantis.csv", "w", encoding='utf-8')
wrote = csv.writer(file, delimiter=';')
header = ['nomen', 'definitio', 'pluma', 'Russian nomen', 'familia', 'Russian nomen familia']
wrote.writerow(header)

for ind in sys.stdin:
    m.append(ind)
for ind in m:
    print(type(ind))
    ind = ind.split('\t')
    a = ind[-1]
    ind[-1] = a[0:len(a) - 1]
    wrote.writerow(ind)