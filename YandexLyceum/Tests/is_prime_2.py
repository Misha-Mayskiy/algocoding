def is_prime(n):
    # Если число меньше или равно 1, понятие "простоты" не определено
    if n <= 1:
        raise ValueError("Простота числа определяется только для n > 1")
    # Перебираем возможные делители от 2 до int(sqrt(n)) включительно
    for divisor in range(2, int(n ** 0.5) + 1):
        if n % divisor == 0:
            return False
    return True


def main():
    try:
        n = int(input().strip())
    except Exception:
        # Если не удалось корректно преобразовать входные данные в число
        print("NO")
        return
    try:
        if is_prime(n):
            print("YES")
        else:
            print("NO")
    except Exception:
        # Если число не удовлетворяет условию n > 1 или иная ошибка
        print("NO")


if __name__ == "__main__":
    main()
