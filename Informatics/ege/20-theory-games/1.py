n = int(input())
events = [tuple(map(int, input().split())) for _ in range(n)]
events.sort(key=lambda x: x[1])

best_rent, best_time, ends = [0], [0], []

for start_i, end_i, rent_i in events:
    j = len(ends) - 1
    while j >= 0 and ends[j] >= start_i:
        j -= 1
    rent = rent_i + best_rent[j + 1]
    time = end_i - start_i + 1 + best_time[j + 1]
    if rent > best_rent[-1]:
        best_rent.append(rent)
        best_time.append(time)
    else:
        best_rent.append(best_rent[-1])
        best_time.append(best_time[-1])
    ends.append(end_i)

print(best_rent[-1], best_time[-1])
