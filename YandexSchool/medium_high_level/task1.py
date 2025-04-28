import sys
from collections import defaultdict


def find_start_end_addresses():
    n = int(sys.stdin.readline())
    if n == 0:
        return "-1"

    addr_counts = defaultdict(int)

    for _ in range(n):
        full_path = sys.stdin.readline().split()
        from_path = full_path[0] + " " + full_path[1]
        to_path = full_path[2] + " " + full_path[3]

        addr_counts[from_path] += 1
        addr_counts[to_path] -= 1

    start_point, end_point = None, None
    start_mb_point, end_mb_point = 0, 0

    for address, start_or_end_addr in addr_counts.items():
        if start_or_end_addr == 1:
            if start_point is not None:
                return "-1"
            start_point = address
            start_mb_point += 1
        elif start_or_end_addr == -1:
            if end_point is not None:
                return "-1"
            end_point = address
            end_mb_point += 1
        elif start_or_end_addr != 0:
            return "-1"

    if start_mb_point == 1 and end_mb_point == 1:
        return f"{start_point} {end_point}"
    else:
        return "-1"


print(find_start_end_addresses())
