import csv


def make_ans(lst):
    ans = list()
    total = 1000
    if int(lst[0][1]) > 1000:
        return 'error'
    ind = 0
    goods = {'0': 0}
    while True:
        if total - int(lst[ind][1]) >= 0 and goods[str(ind)] != 10:
            total -= int(lst[ind][1])
            ans.append(lst[ind][0])
            goods[str(ind)] += 1
        else:
            if ind + 1 == len(lst):
                break
            else:
                ind += 1
                goods[str(ind)] = 0
    return ', '.join(ans)


with open('wares.csv', encoding="utf8") as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='"')
    strings = sorted([x for x in reader], key=lambda x: int(x[1]))

print(make_ans(strings))