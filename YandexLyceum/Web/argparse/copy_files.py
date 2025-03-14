import argparse


def copy_file(source, destination, upper=False, lines=None):
    try:
        with open(source, 'r') as src_file:
            content = src_file.readlines()

            if lines is not None:
                content = content[:lines]

            if upper:
                content = [line.upper() for line in content]

            with open(destination, 'w') as dest_file:
                dest_file.writelines(content)
    except Exception as e:
        print(f"Error while copying: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source', help='Source file name')
    parser.add_argument('destination', help='Destination file name')
    parser.add_argument('--upper', action='store_true', help='Convert text to uppercase')
    parser.add_argument('--lines', type=int, help='Number of lines to copy')

    args = parser.parse_args()

    copy_file(args.source, args.destination, args.upper, args.lines)


if __name__ == '__main__':
    main()
