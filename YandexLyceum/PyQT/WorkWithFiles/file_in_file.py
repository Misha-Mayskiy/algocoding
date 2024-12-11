def to_bytes(size):
    units = {"B": 1, "KB": 1024, "MB": 1024 ** 2, "GB": 1024 ** 3, "TB": 1024 ** 4}
    try:
        num, unit = size.split()
        return int(num) * units[unit]
    except (ValueError, KeyError):
        return 0  # Если данные некорректные, возвращаем 0

def to_largest_unit(size):
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size //= 1024
        i += 1
    return f"{size} {units[i]}"

with open("input.txt", encoding="utf-8") as f:
    lines = [line.strip() for line in f if line.strip()]

groups = {}
for line in lines:
    try:
        name, size = line.rsplit(maxsplit=1)
        ext = name.split(".")[-1]
        groups.setdefault(ext, {"names": [], "size": 0})
        groups[ext]["names"].append(name)
        groups[ext]["size"] += to_bytes(size)
    except ValueError:
        continue  # Игнорируем строки с некорректным форматом

with open("output.txt", "w", encoding="utf-8") as f:
    for ext in sorted(groups):
        for name in sorted(groups[ext]["names"]):
            f.write(name + "\n")
        f.write("----------\n")
        f.write(f"Summary: {to_largest_unit(groups[ext]['size'])}\n\n")
