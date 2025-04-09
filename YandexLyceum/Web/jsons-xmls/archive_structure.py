import zipfile


def print_zip_structure():
    with zipfile.ZipFile('input.zip', 'r') as archive:
        infos = archive.infolist()
        if not infos:
            return
        for info in infos:
            path = info.filename.rstrip('/')
            level = path.count('/')
            name = path.split('/')[-1]
            print("  " * level + name)


if __name__ == '__main__':
    print_zip_structure()
