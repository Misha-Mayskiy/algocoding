import sqlite3

name, db = input(), input()

sql = """
SELECT DISTINCT mags.magic
FROM Magics mags
JOIN Genies gens ON gens.id = mags.genie_id
JOIN Places plas ON plas.genie_id = gens.id
WHERE gens.genie = ? AND mags.hair <= length(plas.place)
"""

rows_of_db = sqlite3.connect(db).execute(sql, (name,)).fetchall()

for wow_magic, in sorted(rows_of_db, reverse=True):
    print(wow_magic)
