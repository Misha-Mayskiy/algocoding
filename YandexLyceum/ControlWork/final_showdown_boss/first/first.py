import sys

dict_answers = {}
for line in sys.stdin:
    number = int(line)
    list_of_divisors = []
    i = 2
    while i * i <= number:
        if number % i == 0:
            list_of_divisors.append(i)
            if i * i != number:
                list_of_divisors.append(number // i)
        i += 1
    dict_answers[number] = sorted(list_of_divisors)

print(dict_answers)
