import sys


def main():
    args = sys.argv[1:]  # Получаем аргументы, исключая имя файла

    if not args:
        print("NO PARAMS")
        return

    result = 0
    sign = 1
    try:
        for arg in args:
            if '.' in arg or arg.isalpha():
                raise ValueError
            if arg.lstrip('-').isdigit():
                result += sign * int(arg)
                sign *= -1
        print(result)
    except Exception as e:
        print(type(e).__name__)


if __name__ == "__main__":
    main()
