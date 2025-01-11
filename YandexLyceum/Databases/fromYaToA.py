import sqlite3


def get_result(database_name):
    """
    Удаляет все фильмы, название которых начинается на букву „Я“ и заканчивается на букву „а“.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    DELETE FROM films
    WHERE title LIKE 'Я%а'
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
