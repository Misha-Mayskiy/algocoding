from itertools import permutations

digits, count = [0, 2, 3, 4, 5, 6, 7], 0
for perm in permutations(digits, 5):
    if all(perm[i] % 2 != perm[i + 1] % 2 for i in range(4)):
        count += 1
print(count)
