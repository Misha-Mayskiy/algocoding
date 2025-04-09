import os
import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel

SCREEN_SIZE = [600, 450]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.getImage()
        self.initUI()

    def getImage(self):
        center = "30.1,59.92"

        # Ломаная линия маршрута Петергоф — Эрмитаж
        route_points = [
            "29.904187,59.884253",  # Петергоф (Большой дворец)
            "29.957273,59.895856",  # Стрельна
            "30.019885,59.906358",  # Южная часть Финского залива
            "30.101295,59.927192",  # Васильевский остров
            "30.165811,59.931688",  # Адмиралтейская набережная
            "30.313509,59.940848"  # Эрмитаж (Зимний дворец)
        ]
        polyline = ",".join(route_points)

        # Параметры карты
        map_request = (
            "https://static-maps.yandex.ru/1.x/"
            f"?ll={center}"
            f"&spn=0.5,0.2"
            f"&l=map"
            f"&pl={polyline}"
        )

        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "gulf_route.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Маршрут Петергоф — Эрмитаж (Финский залив)')

        self.pixmap = QPixmap(self.map_file)
        self.image = QLabel(self)
        self.image.move(0, 0)
        self.image.resize(*SCREEN_SIZE)
        self.image.setPixmap(self.pixmap)

    def closeEvent(self, event):
        os.remove(self.map_file)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
