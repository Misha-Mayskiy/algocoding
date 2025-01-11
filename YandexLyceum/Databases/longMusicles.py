import sqlite3


def get_result(database_name):
    """
    Обновляет длительность мюзиклов, превышающую 100 минут, до 100 минут.

    :param database_name: Имя файла базы данных
    """
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    UPDATE films
    SET duration = 100
    WHERE genre = (
        SELECT id FROM genres
        WHERE title = 'мюзикл'
    ) AND duration > 100
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
