import json
import zipfile


def count_people_in_moscow():
    count = 0
    with zipfile.ZipFile('input.zip', 'r') as archive:
        for info in archive.infolist():
            if info.is_dir():
                continue
            if not info.filename.lower().endswith('.json'):
                continue

            with archive.open(info, 'r') as file:
                try:
                    data = json.load(file)
                    if data.get("city") == "Москва":
                        count += 1
                except Exception:
                    continue

    return count


if __name__ == "__main__":
    print(count_people_in_moscow())
