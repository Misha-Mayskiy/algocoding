import sqlite3


def get_result(database_name):
    """
    Удаляет все фильмы в жанре фантастики, вышедшие до 2000 года, если их длина больше полутора часов.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    DELETE FROM films
    WHERE genre = (
        SELECT id FROM genres
        WHERE title = 'фантастика'
    ) AND year < 2000 AND duration > 90
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
