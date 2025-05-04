import sys

try:
    if len(sys.argv) != 3:
        raise ValueError
    a, b = map(int, sys.argv[1:3])
    print(a + b)
except (ValueError, TypeError):
    print(0)
