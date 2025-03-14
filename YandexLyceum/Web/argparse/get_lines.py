import argparse


def count_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            return sum(1 for _ in file)
    except (FileNotFoundError, PermissionError, IOError, OSError):
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, help='Путь к текстовому файлу')
    args = parser.parse_args()

    print(count_lines(args.file))
