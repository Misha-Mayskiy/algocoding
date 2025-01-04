import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import QRectF


class Square1(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Квадрат-объектив — 1")
        self.setGeometry(100, 100, 800, 900)
        self.color = QColor(0, 0, 255)  # Синий цвет для квадратов

        self.a = 300
        self.k = 0.9
        self.n = 10

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Поля для ввода параметров
        self.lineEdit = QLineEdit(self)
        self.lineEdit.setPlaceholderText("Размер стороны квадрата (по умолчанию 300)")
        self.lineEdit.setText("300")

        self.lineEdit_2 = QLineEdit(self)
        self.lineEdit_2.setPlaceholderText("Коэффициент масштабирования (по умолчанию 0.9)")
        self.lineEdit_2.setText("0.9")

        self.lineEdit_3 = QLineEdit(self)
        self.lineEdit_3.setPlaceholderText("Количество квадратов (по умолчанию 10)")
        self.lineEdit_3.setText("10")

        self.btn = QPushButton("Нарисовать квадраты", self)
        self.btn.clicked.connect(self.draw_squares)

        layout.addWidget(QLabel("Введите параметры:"))
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.lineEdit_2)
        layout.addWidget(self.lineEdit_3)
        layout.addWidget(self.btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def draw_squares(self):
        # Получение параметров из полей ввода
        try:
            self.a = int(self.lineEdit.text())
            self.k = float(self.lineEdit_2.text())
            self.n = int(self.lineEdit_3.text())
        except ValueError:
            return  # Если ввод некорректен, просто выходим из функции

        # Перерисовка окна
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Рисуем квадраты
        for i in range(self.n):
            size = self.a * (self.k ** i)  # Вычисляем размер квадрата
            rect = QRectF(50 + (self.a - size) / 2, 130 + (self.a - size) / 2, size, size)
            painter.setBrush(self.color)
            painter.drawRect(rect)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Square1()
    window.show()
    sys.exit(app.exec())
