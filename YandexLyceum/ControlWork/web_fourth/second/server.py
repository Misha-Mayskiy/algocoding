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
        [191, 135, 88, 198],
        [61, 166, 82, 192],
        [90, 188, 86, 31, 177],
        [91, 4923, 7, 15],
        [58, 129, 45, 19192, 126, 151]
    ]

    server = Server('127.0.0.1', 8080, data)
    with server.run():
        while (row := input('Введите "stop" для завершения работы сервера: ')) != 'stop':
            ...
