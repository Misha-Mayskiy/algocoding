import zipfile


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


def print_zip_structure():
    with zipfile.ZipFile('input.zip', 'r') as archive:
        infos = archive.infolist()
        if not infos:
            return
        for info in infos:
            is_directory = info.filename.endswith('/')
            path = info.filename.rstrip('/')
            level = path.count('/')
            name = path.split('/')[-1]
            if not is_directory:
                size_str = human_read_format(info.file_size)
                print("  " * level + f"{name} {size_str}")
            else:
                print("  " * level + name)


if __name__ == '__main__':
    print_zip_structure()
