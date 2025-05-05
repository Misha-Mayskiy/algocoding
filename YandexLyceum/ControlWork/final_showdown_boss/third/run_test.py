from server import Server
import subprocess, sys, textwrap

stdin_text = textwrap.dedent("""\
    8080
    gourami
    5
""")

srv = Server('127.0.0.1', 8080, [
    {"aqua": "Dutch", "fish": "gourami", "fat": 6},
    {"aqua": "Dutch", "fish": "botsia", "fat": 4},
    {"aqua": "Tropical", "fish": "barbus", "fat": 14},
    {"aqua": "Dutch", "fish": "gourami", "fat": 5},
    {"aqua": "Tropical", "fish": "zebrafish", "fat": 6},
    {"aqua": "Tropical", "fish": "scalaria", "fat": 12},
    {"aqua": "Tropical", "fish": "telescope", "fat": 11},
    {"aqua": "Dutch", "fish": "golden", "fat": 8},
    {"aqua": "Tropical", "fish": "zebrafish", "fat": 8},
    {"aqua": "Japanese", "fish": "zebrafish", "fat": 11}
])

with srv.run():  # сервер поднялся
    proc = subprocess.run(
        [sys.executable, 'fish_filter.py'],
        input=stdin_text.encode(),
        capture_output=True)
    print(proc.stdout.decode())
