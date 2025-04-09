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

    return f"{round(size)}{units[unit_index]}"


def get_directory_size(path):
    total = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                total += os.path.getsize(file_path)
            except Exception:
                pass
    return total


def main():
    base_path = "."
    entries = []

    for entry in os.listdir(base_path):
        full_path = os.path.join(base_path, entry)
        if os.path.isfile(full_path):
            try:
                size = os.path.getsize(full_path)
            except Exception:
                size = 0
        elif os.path.isdir(full_path):
            size = get_directory_size(full_path)
        else:
            continue
        entries.append((entry, size))

    entries.sort(key=lambda x: x[1], reverse=True)

    for name, size in entries[:10]:
        print(f"{name:<50} - {human_read_format(size)}")


if __name__ == "__main__":
    main()
