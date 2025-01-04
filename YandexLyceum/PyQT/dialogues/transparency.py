import sys
import random
from PyQt6.QtWidgets import (QApplication, QMainWindow, QInputDialog, QLabel,
                             QPushButton)
from PyQt6.QtGui import QPainter, QColor, QPixmap


class RandomFlag(QMainWindow):
    def __init__(self):
        super().__init__()

        self.base = [0, 0, 300, 400 // self.get_number_of_colors()]

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Генерация флага')
        self.setGeometry(100, 100, 300, 400)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 300, 400)

        self.button = QPushButton('Ввести количество цветов флага', self)
        self.button.setGeometry(85, 350, 130, 30)
        self.button.clicked.connect(self.generate_flag)

    def get_number_of_colors(self):
        num_colors, ok = QInputDialog.getInt(self, "Количество цветов", "Введите количество цветов флага:", 3, 1, 10, 1)
        if ok:
            return num_colors
        else:
            return 3

    def generate_flag(self):
        num_colors = self.get_number_of_colors()
        self.base[3] = 400 // num_colors

        pixmap = QPixmap(300, 400)
        painter = QPainter(pixmap)

        for i in range(num_colors):
            r = random.randrange(256)
            g = random.randrange(256)
            b = random.randrange(256)
            color = QColor(r, g, b)
            painter.fillRect(0, i * self.base[3], 300, self.base[3], color)

        painter.end()
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RandomFlag()
    ex.show()
    sys.exit(app.exec())
