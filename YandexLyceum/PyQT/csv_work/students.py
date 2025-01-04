import csv

const = int(input())
with open('vps.csv', 'r', encoding='utf8') as input_file:
    reader = csv.reader(input_file, delimiter=";")
    for i in list(reader)[1:]:
        if int(i[-2]) >= const:
            print(i[0])
