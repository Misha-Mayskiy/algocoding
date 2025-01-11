import sqlite3


def get_result(database_name):
    """
    Увеличивает длительность фантастических фильмов вдвое.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    UPDATE films
    SET duration = duration * 2
    WHERE genre = (
        SELECT id FROM genres
        WHERE title = 'фантастика'
    )
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
