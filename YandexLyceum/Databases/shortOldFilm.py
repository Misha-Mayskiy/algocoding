import sqlite3


def get_result(database_name):
    """
    Обновляет длительность фильмов, выпущенных в 1973 году, уменьшая их длину втрое.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    UPDATE films
    SET duration = duration / 3
    WHERE year = 1973
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
