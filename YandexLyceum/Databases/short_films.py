import sqlite3


def get_short_films(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    SELECT title
    FROM films
    WHERE duration <= 85
    """

    cur.execute(query)
    results = cur.fetchall()

    conn.close()

    for row in results:
        print(row[0])


if __name__ == "__main__":
    database_name = input().strip()
    get_short_films(database_name)
