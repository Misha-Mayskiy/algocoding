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
    # Проверка длины пароля
    if len(password) < 9:
        raise LengthError("Password must be at least 9 characters long")

    # Проверка наличия символов разного регистра
    if password.islower() or password.isupper() or password.isdigit():
        raise LetterError("Password must contain both uppercase and lowercase letters")

    # Проверка наличия цифры
    if not any(char.isdigit() for char in password):
        raise DigitError("Password must contain at least one digit")

    # Проверка на наличие запрещённых последовательностей из трех идущих подряд символов
    forbidden_sequences = ['qwertyuiop', 'asdfghjkl', 'zxcvbnm',
                           'йцукенгшщзхъ', 'фывапролджэё', 'ячсмитьбю',
                           '1234567890']
    lower_password = password.lower()
    for sequence in forbidden_sequences:
        for i in range(len(sequence) - 2):
            if sequence[i:i + 3] in lower_password:
                raise SequenceError("Password contains forbidden sequence of three consecutive characters")

    # Если все проверки пройдены, возвращаем 'ok'
    return 'ok'

# check_password("0392040454")
try:
    print(check_password("0392040454"))
except Exception as error:
    print(error.__class__.__name__)