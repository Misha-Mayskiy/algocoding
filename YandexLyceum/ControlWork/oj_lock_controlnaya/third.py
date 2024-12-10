import sqlite3


def magic_eye(db_file, *tools):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    query = """
        SELECT e.witness, m.magician, p.place
        FROM Events e
        JOIN Magicians m ON e.magician_id = m.id
        JOIN Places p ON e.place_id = p.id
        WHERE m.tool IN ({placeholders}) AND e.outcome < 0
        ORDER BY p.place DESC, m.magician ASC, e.witness DESC
    """.format(placeholders=", ".join("?" for _ in tools))

    cur.execute(query, tools)
    results = cur.fetchall()

    conn.close()
    return results


tools = ['wand', 'beard', 'eye']
print(*magic_eye('eye.db', *tools), sep='\n')
