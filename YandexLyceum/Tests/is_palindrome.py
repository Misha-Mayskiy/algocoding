from yandex_testing_lesson import is_palindrome


def main():
    # Список тестовых случаев: пара (строка, ожидаемый результат)
    tests = [
        ("", True),  # пустая строка считается палиндромом
        ("a", True),  # одиночный символ
        ("aba", True),  # обычный палиндром
        ("abba", True),  # четное количество символов
        ("abc", False),  # не палиндром
        ("ab", False),  # не палиндром
        ("Aba", False),  # чувствительность к регистру (если функция чувствительна)
    ]

    for data, expected in tests:
        if is_palindrome(data) != expected:
            print("NO")
            return

    print("YES")


if __name__ == "__main__":
    main()
