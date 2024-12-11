def is_symmetric(sequence, epsilon):
    n = len(sequence)
    for i in range(n // 2):
        if abs(sequence[i] - sequence[n - i - 1]) > epsilon:
            return False
    return True

def find_longest_symmetric_sequence(sequence, epsilon):
    n = len(sequence)
    max_length = 0
    best_sequence = []
    for i in range(n):
        for j in range(i + 1, n + 1):
            sub_sequence = sequence[i:j]
            if is_symmetric(sub_sequence, epsilon):
                if len(sub_sequence) > max_length:
                    max_length = len(sub_sequence)
                    best_sequence = sub_sequence
    return best_sequence

sequence = list(map(float, input().split()))
epsilon = float(input())
result = find_longest_symmetric_sequence(sequence, epsilon)
print(" ".join(map(str, result)))
