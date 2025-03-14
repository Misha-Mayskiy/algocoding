import argparse

try:
    parser = argparse.ArgumentParser()
    parser.add_argument('numbers', nargs='*', help='Two integers to sum')

    args = parser.parse_args()

    if len(args.numbers) == 0:
        print("NO PARAMS")
    elif len(args.numbers) == 1:
        print("TOO FEW PARAMS")
    elif len(args.numbers) > 2:
        print("TOO MANY PARAMS")
    else:
        try:
            num1 = int(args.numbers[0])
            num2 = int(args.numbers[1])
            print(num1 + num2)
        except Exception as e:
            print(e.__class__.__name__)
except Exception as e:
    print(e.__class__.__name__)
