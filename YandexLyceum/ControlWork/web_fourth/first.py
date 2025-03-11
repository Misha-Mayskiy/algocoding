import json


def checking_word(word):
    letters = "aeyuio"
    counter = sum(1 for char in word.lower() if char in letters)

    return (len(word) % 2) == (counter % 2)


res, line_number, flag = {}, 1, 1
while flag:
    try:
        line = input()
        words = line.split()
        filtered_words = [word for word in words if checking_word(word)]

        if filtered_words:
            res[str(line_number)] = filtered_words

        line_number += 1
    except EOFError:
        flag = 0

with open('broom.json', 'w') as file:
    json.dump(res, file, indent=4)
