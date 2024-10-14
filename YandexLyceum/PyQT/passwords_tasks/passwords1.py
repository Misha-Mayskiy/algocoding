import sys


def get_keyboard_sequences():
    # Определение последовательностей для английской раскладки (PC и Mac)
    en_pc_rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    en_mac_rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm"
    ]

    # Определение последовательностей для русской раскладки (PC и Mac)
    ru_pc_rows = [
        "йцукенгшщзхъ",
        "фывапролджэ",
        "ячсмитьбю"
    ]

    ru_mac_rows = [
        "йцукенгшщзхъ",
        "фывапролджэ",
        "ячсмитьбю"
    ]

    all_rows = en_pc_rows + en_mac_rows + ru_pc_rows + ru_mac_rows

    sequences = set()

    for row in all_rows:
        row_lower = row.lower()
        for i in range(len(row_lower) - 2):
            seq = row_lower[i:i + 3]
            sequences.add(seq)
            sequences.add(seq[::-1])  # Добавляем обратную последовательность

    return sequences


def has_keyboard_sequence(password, sequences):
    password_lower = password.lower()
    for i in range(len(password_lower) - 2):
        substr = password_lower[i:i + 3]
        if substr in sequences:
            return True
    return False


def is_upper(char):
    return char.isupper()


def is_lower(char):
    return char.islower()


def has_upper_and_lower(password):
    has_uppercase = False
    has_lowercase = False
    for char in password:
        if char.isupper():
            has_uppercase = True
        elif char.islower():
            has_lowercase = True
        if has_uppercase and has_lowercase:
            return True
    return False


def has_digit(password):
    for char in password:
        if char.isdigit():
            return True
    return False


def main():
    password = sys.stdin.read().strip()

    # Критерий 1: Длина пароля > 8
    if len(password) <= 8:
        print("error")
        return

    # Критерий 2: Наличие заглавных и строчных букв
    if not has_upper_and_lower(password):
        print("error")
        return

    # Критерий 3: Наличие хотя бы одной цифры
    if not has_digit(password):
        print("error")
        return

    # Критерий 4: Отсутствие запрещенных последовательностей
    sequences = get_keyboard_sequences()
    if has_keyboard_sequence(password, sequences):
        print("error")
        return

    # Если все критерии удовлетворены
    print("ok")


if __name__ == "__main__":
    main()
