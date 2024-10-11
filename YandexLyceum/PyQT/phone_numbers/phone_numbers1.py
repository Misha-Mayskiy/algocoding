def validate_and_format_phone_number(phone):
    phone = phone.strip()
    if phone.count('(') > 1 or phone.count(')') > 1 or phone.find('(') > phone.find(')'):
        return "error"

    phone = phone.replace(" ", "").replace("\t", "")
    if '--' in phone or phone.startswith('-') or phone.endswith('-'):
        return "error"

    phone = phone.replace("(", "").replace(")", "").replace("-", "")

    if phone.startswith('+7'):
        phone = phone[2:]
    elif phone.startswith('8'):
        phone = phone[1:]
    else:
        return "error"

    if not phone.isdigit() or len(phone) != 10:
        return "error"
    return f"+7{phone}"


print(validate_and_format_phone_number(input()))
