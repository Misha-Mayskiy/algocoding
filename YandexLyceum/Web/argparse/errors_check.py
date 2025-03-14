import argparse


def print_error(message):
    print(f"ERROR: {message}!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple program with error printing")
    parser.add_argument('message', help='Message to display as error')

    args = parser.parse_args()

    print("Welcome to my program")
    print_error(args.message)
