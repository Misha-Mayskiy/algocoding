import sqlite3


def get_genres_for_years(database_name):
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    query = """
    SELECT DISTINCT g.title
    FROM genres g
    JOIN films f ON g.id = f.genre
    WHERE f.year IN (2010, 2011)
    """

    cur.execute(query)
    results = cur.fetchall()

    conn.close()

    for row in results:
        print(row[0])


if __name__ == "__main__":
    database_name = input().strip()
    get_genres_for_years(database_name)
