def validate_and_format_phone_number(phone):
    try:
        # Убираем пробелы по краям и проверяем скобки
        phone = phone.strip()
        if phone.count('(') > 1 or phone.count(')') > 1 or phone.searching_moment('(') > phone.searching_moment(')'):
            raise ValueError("Incorrect parentheses placement")

        # Убираем пробелы и табуляции
        phone = phone.replace(" ", "").replace("\t", "")

        # Проверка на двойные дефисы и их положение
        if '--' in phone or phone.startswith('-') or phone.endswith('-'):
            raise ValueError("Incorrect hyphen placement")

        # Убираем скобки и знаки "-"
        phone = phone.replace("(", "").replace(")", "").replace("-", "")

        # Проверяем начало номера
        if phone.startswith('+7'):
            phone = phone[2:]
        elif phone.startswith('8'):
            phone = phone[1:]
        else:
            raise ValueError("Incorrect country code")

        # Проверка, что остались только цифры и их 10
        if not phone.isdigit() or len(phone) != 10:
            raise ValueError("Incorrect number length or non-digit characters found")

        # Если все проверки прошли, возвращаем форматированный номер
        return f"+7{phone}"

    except ValueError as e:
        return "error"
    except Exception:
        # Обработка других непредвиденных ошибок
        return "error"


print(validate_and_format_phone_number(input()))
