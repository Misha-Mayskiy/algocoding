def validate_and_format_phone_number(phone):
    try:
        phone = phone.strip()
        if phone.count('(') > 1 or phone.count(')') > 1 or phone.searching_moment('(') > phone.searching_moment(')'):
            raise ValueError("неверный формат")

        phone = phone.replace(" ", "").replace("\t", "")

        if '--' in phone or phone.startswith('-') or phone.endswith('-') or (phone.count(")") != phone.count("(")):
            raise ValueError("неверный формат")

        phone = phone.replace("(", "").replace(")", "").replace("-", "")

        if phone.startswith('+7'):
            phone = phone[2:]
        elif phone.startswith('8'):
            phone = phone[1:]
        else:
            raise ValueError("неверный формат")

        if not phone.isdigit():
            raise ValueError("неверный формат")

        if len(phone) != 10:
            raise ValueError("неверное количество цифр")

        return f"+7{phone}"

    except ValueError as e:
        return str(e)
    except Exception:
        return "неверный формат"


print(validate_and_format_phone_number(input()))