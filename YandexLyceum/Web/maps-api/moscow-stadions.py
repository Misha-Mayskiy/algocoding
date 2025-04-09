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
        # Центр карты — Москва
        center = "37.620070,55.753630"
        # Метки: Спартак, Динамо, Лужники
        placemarks = [
            "37.440938,55.817192,pm2rdm",  # Спартак
            "37.559444,55.790278,pm2blm",  # Динамо
            "37.553333,55.715833,pm2grm",  # Лужники
        ]
        pts = "~".join(placemarks)

        map_request = (
            f"http://static-maps.yandex.ru/1.x/"
            f"?ll={center}&spn=0.2,0.2&l=map&pt={pts}"
        )

        response = requests.get(map_request)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_request)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)

    def initUI(self):
        self.setGeometry(100, 100, *SCREEN_SIZE)
        self.setWindowTitle('Карта Москвы со стадионами')

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
