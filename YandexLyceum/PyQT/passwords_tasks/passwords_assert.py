# Определяем базовый класс исключений для паролей
class PasswordError(Exception):
    pass


# Определяем конкретные классы исключений для разных нарушений
class LengthError(PasswordError):
    pass


class LetterError(PasswordError):
    pass


class DigitError(PasswordError):
    pass


class SequenceError(PasswordError):
    pass


# Функция проверки пароля
def check_password(password):
    assert len(password) >= 9, LengthError("Password must be at least 9 characters long")

    assert not (password.islower() or password.isupper() or password.isdigit()), \
        LetterError("Password must contain both uppercase and lowercase letters")

    assert any(char.isdigit() for char in password), DigitError("Password must contain at least one digit")

    forbidden_sequences = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm',
                           'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю',
                           '1234567890']
    lower_password = password.lower()
    for sequence in forbidden_sequences:
        for i in range(len(sequence) - 2):
            assert sequence[i:i + 3] not in lower_password, \
                SequenceError("Password contains forbidden sequence of three consecutive characters")

    return 'ok'


try:
    password = input()
    result = check_password(password)
    print(result)
except AssertionError as error:
    print("error")
except Exception as error:
    print("error")
