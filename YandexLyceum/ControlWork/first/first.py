def process_lines(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            words = line.strip().split()  # Разделяем строку на слова
            unique_words = []  # Список для хранения уникальных слов
            seen = set()  # Множество для отслеживания уже добавленных слов

            for word in words:
                if word not in seen:
                    seen.add(word)
                    unique_words.append(word)
                else:
                    seen.remove(word)
                    unique_words.remove(word)

            # Записываем уникальные слова в выходной файл
            outfile.write(' '.join(unique_words) + '\n')


# Задаем имя входного и выходного файла
input_file = 'lines.txt'
output_file = 'reflect.txt'

# Запускаем обработку
process_lines(input_file, output_file)
