import sys
from math import cos, pi, sin

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QInputDialog, QColorDialog

SCREEN_SIZE = [500, 500]
SIDE_LENGTH = 100
SIDES_COUNT = 8


class Square2(QWidget):
    def __init__(self):
        super().__init__()
        self.m = 0
        self.flag = False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, *SCREEN_SIZE)
        self.setWindowTitle('Рисуем')
        self.button_1 = QPushButton(self)
        self.button_1.move(0, 0)
        self.button_1.setText("Чертить")
        self.button_1.clicked.connect(self.run)

    def run(self):
        global SIDES_COUNT
        k, ok_pressed = QInputDialog.getText(self, "Переменные", "K")
        if ok_pressed:
            self.k = float(k)
        N, ok_pressed1 = QInputDialog.getText(self, "Переменные", "N")
        if ok_pressed1:
            SIDES_COUNT = int(N)
        M, ok_pressed2 = QInputDialog.getText(self, "Переменные", "M")
        if ok_pressed2:
            self.m = int(M)
        color = QColorDialog.getColor()
        if color.isValid():
            self.color = color.name()
            self.flag = True
            self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_star(qp)
        qp.end()

    def xs(self, x):
        return x + SCREEN_SIZE[0] // 2

    def ys(self, y):
        return SCREEN_SIZE[1] // 2 - y

    def draw_star(self, qp):
        if self.flag:
            pen = QPen(QColor(self.color), 2)
            qp.setPen(pen)
            nodes = [(SIDE_LENGTH * cos(i * 2 * pi / SIDES_COUNT),
                      SIDE_LENGTH * sin(i * 2 * pi / SIDES_COUNT))
                     for i in range(SIDES_COUNT)]
            nodes2 = [(int(self.xs(node[0])),
                       int(self.ys(node[1]))) for node in nodes]
            for i in range(self.m):
                n = 0
                a = (0, 0)
                for y in range(-1, len(nodes2) - 1):
                    n += 1
                    if n == 1:
                        a = nodes2[y]
                    if n == SIDES_COUNT:
                        qp.drawLine(*nodes2[y], *a)
                        nodes2[y] = (int((nodes2[y][0] + self.k * a[0]) / (self.k + 1)),
                                     int((nodes2[y][1] + self.k * a[1]) / (self.k + 1)))
                    else:
                        qp.drawLine(*nodes2[y], *nodes2[y + 1])
                        nodes2[y] = (int((nodes2[y][0] + self.k * nodes2[y + 1][0]) / (self.k + 1)),
                                     int((nodes2[y][1] + self.k * nodes2[y + 1][1]) / (self.k + 1)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Square2()
    ex.show()
    sys.exit(app.exec())