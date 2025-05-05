import csv
import sqlite3
from flask import Flask
from flask import jsonify

TREASURES = []
with open('wealth.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f, delimiter='.'):
        TREASURES.append(
            (
                r['item'],
                int(r['size']),
                int(r['value']),
                r['material'].lower(),
                r['decoration'].lower(),
            )
        )


def sort_key(t):
    return -t[2], t[0]


app = Flask(__name__)


@app.route('/advantage/<name>/')
def loot(name):
    with sqlite3.connect('owners.db') as db:
        cur = db.cursor()

        tid_row = cur.execute(
            'SELECT type_id FROM Masters WHERE name=?', (name,)
        ).fetchone()
        if not tid_row:
            return jsonify([])

        size_row = cur.execute(
            'SELECT size FROM Preferences WHERE id=?', tid_row
        ).fetchone()
        if not size_row:
            return jsonify([])

        need = size_row[0]

    prudik = [
        x
        for x in TREASURES
        if x[1] > need and ('gold' in x[3] or 'gold' in x[4])
    ]
    prudik.sort(key=sort_key)

    if not prudik:
        return jsonify([])

    result = [x[0] for x in prudik[:5]]
    edge_value = prudik[4][2] if len(prudik) >= 5 else None

    if edge_value is not None:
        result += [x[0] for x in prudik[5:] if x[2] == edge_value]

    return jsonify(result)


if __name__ == '__main__':
    app.run('127.0.0.1', 8080)
