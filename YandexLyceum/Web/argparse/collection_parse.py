import argparse


def main():
    parser = argparse.ArgumentParser(description='Обработка аргументов вида ключ=значение')
    parser.add_argument('--sort', action='store_true', help='сортировать вывод по ключу')

    args, unknown_args = parser.parse_known_args()

    key_value_pairs = {}
    for arg in unknown_args:
        if '=' in arg:
            key, value = arg.split('=', 1)  # Разделяем по первому знаку =
            key_value_pairs[key] = value

    keys = sorted(key_value_pairs.keys()) if args.sort else key_value_pairs.keys()

    for key in keys:
        print(f"Key: {key}\tValue: {key_value_pairs[key]}")


if __name__ == "__main__":
    main()
