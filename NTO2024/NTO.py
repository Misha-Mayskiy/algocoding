def count_divisors(num):
    count = 0
    for i in range(1, num // 2 + 1):
        if num % i == 0:
            count += 1
            if i != num // i:  # Если делитель не равен квадрату числа
                count += 1
    return count

def check_conditions(n):
    if n % 2 != 0:
        return False  # n должно быть четным

    d_o = 0  # Количество нечетных делителей
    d_e = 0  # Количество четных делителей
    for i in range(1, n + 1):
        if n % i == 0:
            if i % 2 == 0:
                d_e += 1
            else:
                d_o += 1

    if d_e != 5 * d_o:
        return False

    d_total = d_e + d_o
    if d_total % 3 != 0 or d_o == 0:
        return False

    # Проверяем, что половина четных делителей делится на 5
    if d_e % 2 != 0 or (d_e // 2) % 2 != 0:
        return False

    return True

max_number = 0

for n in range(1, 10001):
    if check_conditions(n):
        max_number = n

print(max_number)
