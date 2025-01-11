import sqlite3


def get_result(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    DELETE FROM films
    WHERE genre = (
        SELECT id FROM genres
        WHERE title = 'комедия'
    )
    """

    cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    database_name = input().strip()
    get_result(database_name)
