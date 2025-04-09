import os


def human_read_format(size):
    units = ["Б", "КБ", "МБ", "ГБ"]
    factor = 1024

    if size == 0:
        return "0" + units[0]

    unit_index = 0
    while size >= factor and unit_index < len(units) - 1:
        size /= factor
        unit_index += 1

    size = round(size)
    return str(size) + units[unit_index]


def get_files_sizes():
    result = []
    for filename in os.listdir('.'):
        if os.path.isfile(filename):
            size_bytes = os.path.getsize(filename)
            readable = human_read_format(size_bytes)
            result.append(f"{filename} {readable}")
    return '\n'.join(result)


if __name__ == "__main__":
    print(get_files_sizes())
