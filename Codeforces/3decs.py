t = int(input())
for i in range(t):
    a, b, c = map(int, input().split())
    if (c >= abs(a - b)) and (c - abs(a - b) >= max(a, b)) and ((c - abs(a - b) - max(a, b)) % 3 == 0):
        print("YES")
    else:
        print("NO")