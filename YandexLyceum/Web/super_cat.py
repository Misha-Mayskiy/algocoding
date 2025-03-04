import sys
import os

try:
    args = sys.argv[1:]

    if not args:
        print("ERROR")
        sys.exit(1)

    filename = args[-1]
    flags = args[:-1]

    if not os.path.exists(filename):
        print("ERROR")
        sys.exit(1)

    with open(filename, 'r') as f:
        lines = [line.rstrip('\n') for line in f]

    sort_flag = '--sort' in flags
    count_flag = '--count' in flags
    num_flag = '--num' in flags

    if sort_flag:
        lines.sort()

    if num_flag:
        numbered_lines = [f"{i} {line}" for i, line in enumerate(lines)]
    else:
        numbered_lines = lines.copy()

    for line in numbered_lines:
        print(line)

    if count_flag:
        print(f"rows count: {len(lines)}")

except Exception:
    print("ERROR")
    sys.exit(1)