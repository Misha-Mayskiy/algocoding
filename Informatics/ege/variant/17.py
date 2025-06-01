def process_sequence(seq):
    m_cands = [x for x in seq if 100 <= abs(x) <= 999 and abs(x) % 100 == 15]
    m = min(m_cands)
    threshold = m * m

    count = 0
    min_prod = None

    for i in range(len(seq) - 2):
        a, b, c = seq[i], seq[i+1], seq[i+2]
        if (a > 0 and b > 0 and c > 0) or (a < 0 and b < 0 and c < 0):
            mn, mx = min(a, b, c), max(a, b, c)
            prod = mn * mx
            if prod > threshold:
                count += 1
                if min_prod is None or prod < min_prod:
                    min_prod = prod

    return count, min_prod


if __name__ == "__main__":
    with open("input.txt") as f:
        seq = [int(line) for line in f]

    cnt, min_elem = process_sequence(seq)
    print(cnt, min_elem)
