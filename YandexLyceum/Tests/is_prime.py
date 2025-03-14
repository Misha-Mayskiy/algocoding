from yandex_testing_lesson import is_prime


def main():
    # Тестовые случаи для корректных значений n > 1
    tests = [
        (2, True),  # 2 — простое число
        (3, True),  # 3 — простое число
        (4, False),  # 4 — составное число
        (5, True),  # 5 — простое число
        (6, False),  # 6 — составное число
        (7, True),  # 7 — простое число
        (11, True),  # 11 — простое число
        (12, False),  # 12 — составное число
    ]

    for n, expected in tests:
        try:
            result = is_prime(n)
        except Exception:
            print("NO")
            return
        if result != expected:
            print("NO")
            return

    # Тестовые случаи для некорректных значений (n <= 1 или отрицательные)
    invalid_tests = [0, 1, -1, -10]
    for n in invalid_tests:
        try:
            # Ожидается, что функция вызовет исключение
            is_prime(n)
        except Exception:
            continue  # исключение вызвано — всё верно
        else:
            # Если исключение не вызвано, то тест не пройден
            print("NO")
            return

    print("YES")


if __name__ == "__main__":
    main()
