import sqlite3


def get_result(database_name):
    """
    Обновляет информацию о фильмах: поле с длительностью фильма, если оно изначально пустое (пустая строка),
    должно стать равным 42 минутам.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    UPDATE films
    SET duration = 42
    WHERE duration = ''
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
