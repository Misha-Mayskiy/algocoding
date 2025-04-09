import os
import zipfile
from datetime import datetime


def make_reserve_arc(from_save, to_save):
    if not os.path.isdir(from_save):
        raise ValueError(f"Указанный исходный каталог не существует: {from_save}")

    if not os.path.isdir(to_save):
        os.makedirs(to_save, exist_ok=True)

    date_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"backup_{date_time_str}.zip"
    archive_path = os.path.join(to_save, archive_name)

    with zipfile.ZipFile(archive_path, mode='w', compression=zipfile.ZIP_DEFLATED) as archive:
        for root, dirs, files in os.walk(from_save):
            for file in files:
                full_path = os.path.join(root, file)
                relative_path = os.path.relpath(full_path, from_save)
                archive.write(full_path, arcname=relative_path)

    print(f"Архив создан: {archive_path}")
    return archive_path


if __name__ == "__main__":
    source = input("Введите путь к каталогу, который требуется архивировать: ").strip()
    dest = input("Введите путь к каталогу, в который сохранить резервную копию: ").strip()

    try:
        make_reserve_arc(source, dest)
    except Exception as e:
        print(f"Ошибка: {e}")
