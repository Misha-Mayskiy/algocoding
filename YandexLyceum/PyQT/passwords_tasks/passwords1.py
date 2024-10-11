def is_good_password(password):
    # Клавиатурные строки для проверки запрещенных последовательностей
    layouts = [
        "qwertyuiop", "asdfghjkl", "zxcvbnm",  # QWERTY
        "йцукенгшщзхъ", "фывапролджэ", "ячсмитьбю"  # ЙЦУКЕН
    ]

    # 1. Проверка длины пароля
    if len(password) <= 8:
        return "error"

    # 2. Проверка наличия хотя бы одной заглавной и строчной буквы
    has_upper = any(char.isupper() for char in password)
    has_lower = any(char.islower() for char in password)
    if not has_upper or not has_lower:
        return "error"

    # 3. Проверка наличия хотя бы одной цифры
    has_digit = any(char.isdigit() for char in password)
    if not has_digit:
        return "error"

    # 4. Проверка на запрещенные последовательности букв
    password_lower = password.lower()  # переводим в нижний регистр для упрощения проверки
    for layout in layouts:
        # Проходим по всем возможным 3-буквенным комбинациям в каждом раскладе
        for i in range(len(layout) - 2):
            sequence = layout[i:i + 3]
            if sequence in password_lower:
                return "error"

    return "ok"


# Примеры тестов
print(is_good_password(input()))