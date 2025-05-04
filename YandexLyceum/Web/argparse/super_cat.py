import os
import sys


def main():
    args = sys.argv[1:]

    count_flag = "--count" in args
    num_flag = "--num" in args
    sort_flag = "--sort" in args

    if count_flag:
        args.remove("--count")
    if num_flag:
        args.remove("--num")
    if sort_flag:
        args.remove("--sort")

    if not args:
        print("ERROR")
        return

    filename = args[0]

    if not os.path.isfile(filename):
        print("ERROR")
        return

    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        lines = [line.rstrip('\n') for line in lines]

        if sort_flag:
            lines.sort()

        for i, line in enumerate(lines):
            if num_flag:
                print(f"{i} {line}")
            else:
                print(line)

        if count_flag:
            print(f"rows count: {len(lines)}")

    except Exception:
        print("ERROR")


if __name__ == "__main__":
    main()
