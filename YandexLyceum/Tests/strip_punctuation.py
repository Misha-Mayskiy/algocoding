from yandex_testing_lesson import strip_punctuation_ru


def test_strip_punctuation_ru():
    test_cases = [
        ("Привет, мир!", "Привет мир"),
        ("Точка. Запятая, Восклицание! Вопрос?", "Точка Запятая Восклицание Вопрос"),
        ("Кто-то позвонил в дверь.", "Кто-то позвонил в дверь"),
        ("Из-за шума я не мог заснуть.", "Из-за шума я не мог заснуть"),
        ("В 2023 году было 365 дней.", "В 2023 году было 365 дней"),
        ("Слово - слово", "Слово слово"),
        ("Слово— слово", "Слово слово")
    ]

    for input_str, expected_output in test_cases:
        result = strip_punctuation_ru(input_str)
        if result != expected_output:
            return False

    return True


if __name__ == "__main__":
    if test_strip_punctuation_ru():
        print("YES")
    else:
        print("NO")
