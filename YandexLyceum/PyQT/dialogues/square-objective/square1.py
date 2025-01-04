import sys

from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit


class Square1(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(0, 0, 500, 570)
        self.setWindowTitle('Квадрат объектив 1')

        self.show_square = QPushButton('Показать', self)
        self.show_square.resize(100, 30)
        self.show_square.move(10, 15)
        self.do_paint = False
        self.show_square.clicked.connect(self.paint)

        self.side_text = QLabel(self)
        self.side_text.setText('side')
        self.side_text.move(200, 15)

        self.coeff_text = QLabel(self)
        self.coeff_text.setText('coeff')
        self.coeff_text.move(200, 50)

        self.n_text = QLabel(self)
        self.n_text.setText('n')
        self.n_text.move(200, 85)

        self.side = QLineEdit(self)
        self.side.resize(150, 25)
        self.side.move(250, 15)

        self.coeff = QLineEdit(self)
        self.coeff.resize(150, 25)
        self.coeff.move(250, 50)

        self.n = QLineEdit(self)
        self.n.resize(150, 25)
        self.n.move(250, 85)

    def paintEvent(self, event):
        if self.do_paint:
            qp = QPainter()
            qp.begin(self)
            self.draw(qp)
            qp.end()

    def paint(self, event):
        self.do_paint = True
        self.repaint()

    def draw(self, qp):
        current_side = int(self.side.text())
        for _ in range(int(self.n.text())):
            current_side = int(current_side)
            qp.setPen(QColor(255, 0, 0))
            qp.drawRect(250 - (int(current_side) // 2),
                        345 - (int(current_side) // 2),
                        int(current_side),
                        int(current_side))
            current_side *= float(self.coeff.text())
        self.do_paint = False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Square1()
    ex.show()
    sys.exit(app.exec())
