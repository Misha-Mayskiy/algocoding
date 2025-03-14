import re


def is_correct_mobile_phone_ru(number: str) -> bool:
    cleaned = number.replace(" ", "").replace("-", "")

    pattern1 = r'^8\d{10}$'
    pattern2 = r'^8\(\d{3}\)\d{7}$'
    pattern3 = r'^\+7\d{10}$'
    pattern4 = r'^\+7\(\d{3}\)\d{7}$'

    if re.match(pattern1, cleaned) or re.match(pattern2, cleaned) or \
            re.match(pattern3, cleaned) or re.match(pattern4, cleaned):
        return True
    return False


def main():
    try:
        phone = input().strip()
    except Exception:
        print("NO")
        return

    if is_correct_mobile_phone_ru(phone):
        print("YES")
    else:
        print("NO")


if __name__ == "__main__":
    main()
