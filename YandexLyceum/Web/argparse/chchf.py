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
