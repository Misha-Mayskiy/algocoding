transliteration_table = {
    "й": "j", "ц": "c", "у": "u", "к": "k", "е": "e", "н": "n",
    "г": "g", "ш": "sh", "щ": "shh", "з": "z", "х": "h", "ъ": "#",
    "ф": "f", "ы": "y", "в": "v", "а": "a", "п": "p", "р": "r",
    "о": "o", "л": "l", "д": "d", "ж": "zh", "э": "je", "я": "ya",
    "ч": "ch", "с": "s", "м": "m", "и": "i", "т": "t", "ь": "'",
    "б": "b", "ю": "ju", "ё": "jo"
}


def transliterate(text):
    result = []
    i = 0
    while i < len(text):
        char = text[i]
        is_upper = char.isupper()
        lower_char = char.lower()
        if lower_char in transliteration_table:
            transliterated_char = transliteration_table[lower_char]
            if is_upper:
                transliterated_char = transliterated_char.capitalize()
            result.append(transliterated_char)
        else:
            result.append(char)
        i += 1
    return ''.join(result)


# Чтение из файла и запись в новый файл
with open('cyrillic.txt', encoding='utf-8') as infile:
    text = infile.read()

transliterated_text = transliterate(text)

with open('transliteration.txt', 'w', encoding='utf-8') as outfile:
    outfile.write(transliterated_text)
