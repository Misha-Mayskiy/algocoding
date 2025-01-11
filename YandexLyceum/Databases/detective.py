import sqlite3


def get_detective_films(database_name):
    # Подключаемся к базе данных
    conn = sqlite3.connect(database_name)
    cur = conn.cursor()

    # Формируем SQL-запрос
    query = """
    SELECT title FROM Films
    WHERE genre = (
        SELECT id FROM genres
        WHERE title = 'детектив'
    ) AND year BETWEEN 1995 AND 2000
    """

    # Выполняем запрос
    cur.execute(query)
    results = cur.fetchall()

    # Закрываем соединение
    conn.close()

    # Выводим результаты
    for row in results:
        print(row[0])


# Считываем имя базы данных
database_name = input().strip()

# Вызываем функцию для получения списка фильмов
get_detective_films(database_name)
