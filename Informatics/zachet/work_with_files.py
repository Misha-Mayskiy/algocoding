# Открытие файла для чтения
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)

# Открытие файла для чтения с чтением каждой строки
with open('example.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        print(line.strip())  # strip() удаляет символы новой строки

# Открытие файла для записи (создаст файл, если он не существует)
with open('example.txt', 'w') as file:
    file.write('Hello, World!\n')
    file.write('This is a new line.\n')

# Открытие файла для добавления (добавит данные в конец файла)
with open('example.txt', 'a') as file:
    file.write('This is an appended line.\n')

# Открытие файла для чтения бинарных данных
with open('example.bin', 'rb') as file:
    binary_data = file.read()
    print(binary_data)

# Открытие файла для записи бинарных данных
with open('example.bin', 'wb') as file:
    file.write(b'Hello, World!')

# Открытие файла с использованием менеджера контекста
with open('example.txt', 'r') as file:
    content = file.read()
    print(content)
# Файл автоматически закрывается после завершения блока with
