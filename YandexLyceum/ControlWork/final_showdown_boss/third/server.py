import io
import logging
from contextlib import contextmanager, redirect_stdout
from json import dumps
from multiprocessing import Process
from time import sleep

from flask import Flask

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Server:
    def __init__(self, host, port, data):
        self.__host__ = host
        self.__port__ = port
        self.__data__ = data

    @contextmanager
    def run(self):
        p = Process(target=self.server)
        p.start()
        sleep(1)
        yield
        p.kill()

    def server(self):
        _ = io.StringIO()
        with redirect_stdout(_):
            app = Flask(__name__)

            @app.route('/')
            def index():
                return dumps(self.__data__)

            app.run(self.__host__, self.__port__)


if __name__ == '__main__':
    data = [
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
    ]

    server = Server('127.0.0.1', 8080, data)
    with server.run():
        while (row := input('Введите "stop" для завершения работы сервера: ')) != 'stop':
            ...
