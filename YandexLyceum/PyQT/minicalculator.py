import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QLCDNumber


class MiniCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 375, 150)
        self.setWindowTitle('Вычисление выражений')

        self.number_1 = QLineEdit(self)
        self.number_1.move(10, 10)

        self.calculate_button = QPushButton("->", self)
        self.calculate_button.resize(self.calculate_button.sizeHint())
        self.calculate_button.move(150, 8)
        self.calculate_button.clicked.connect(self.calculation)

        self.number_2 = QLineEdit(self)
        self.number_2.move(10, 50)

        self.result_sum = QLCDNumber(self)
        self.result_sum.move(250, 10)
        self.result_sub = QLCDNumber(self)
        self.result_sub.move(250, 35)
        self.result_mul = QLCDNumber(self)
        self.result_mul.move(250, 60)
        self.result_div = QLCDNumber(self)
        self.result_div.move(250, 85)

    def calculation(self):
        self.result_sum.display(str(eval(f"{self.number_1.text()} + {self.number_2.text()}")))
        self.result_sub.display(str(eval(f"{self.number_1.text()} - {self.number_2.text()}")))
        self.result_mul.display(str(eval(f"{self.number_1.text()} * {self.number_2.text()}")))
        if self.number_2.text() == "0":
            self.result_div.display("Error")
        else:
            self.result_div.display(str(round(eval(f"{self.number_1.text()} / {self.number_2.text()}"), 3)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MiniCalculator()
    ex.show()
    sys.exit(app.exec())
