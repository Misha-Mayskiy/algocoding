import argparse
import os


def main():
    parser = argparse.ArgumentParser(description='Программа для вывода содержимого файла')

    parser.add_argument('filename', help='имя файла для чтения')
    parser.add_argument('--count', action='store_true', help='вывести количество строк в конце')
    parser.add_argument('--num', action='store_true', help='вывести номера строк')
    parser.add_argument('--sort', action='store_true', help='отсортировать строки по алфавиту')

    args = parser.parse_args()

    if not os.path.isfile(args.filename):
        print("ERROR")
        return

    try:
        with open(args.filename, 'r') as file:
            lines = file.read().splitlines()
    except (IOError, PermissionError):
        print("ERROR")
        return

    if args.sort:
        lines.sort()

    for i, line in enumerate(lines):
        if args.num:
            print(f"{i} {line}")
        else:
            print(line)

    if args.count:
        print(f"rows count: {len(lines)}")


if __name__ == "__main__":
    main()
