n = int(input())
a = list(map(int, input().split()))
b = list(map(int, input().split()))
c = list(map(int, input().split()))
x0, y0 = map(int, input().split())

dp = [[[0, 0, 0], [0, 0, 0]] for _ in range(n + 1)]
dp[0][0] = [x0 + y0, x0, y0]
dp[0][1] = [x0 + y0, x0, y0]

for step in range(1, n + 1):
    a_val = a[step - 1]
    b_val = b[step - 1]
    c_val = c[step - 1]
    for current_option in range(2):
        best_sum = -1
        best_x = 0
        best_y = 0
        for prev_option in range(2):
            prev_x = dp[step - 1][prev_option][1]
            prev_y = dp[step - 1][prev_option][2]
            prev_sum = dp[step - 1][prev_option][0]
            if current_option == 0:
                temp_x = min(prev_x + a_val, b_val)
                temp_y = prev_y + a_val
            else:
                temp_x = prev_x + a_val
                temp_y = min(prev_y + a_val, c_val)
            current_sum = prev_sum + (temp_x - prev_x) + (temp_y - prev_y)
            if current_sum > best_sum:
                best_sum = current_sum
                best_x = temp_x
                best_y = temp_y
        dp[step][current_option] = [best_sum, best_x, best_y]

result = max(dp[n][0][0], dp[n][1][0])
print(result)
