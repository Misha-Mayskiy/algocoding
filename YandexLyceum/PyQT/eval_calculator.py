import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit


class Evaluator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 375, 50)
        self.setWindowTitle('Вычисление выражений')

        self.first_value = QLineEdit(self)
        self.first_value.move(10, 10)

        self.trick_button = QPushButton("->", self)
        self.trick_button.resize(self.trick_button.sizeHint())
        self.trick_button.move(150, 8)
        self.trick_button.clicked.connect(self.calculation)

        self.second_value = QLineEdit(self)
        self.second_value.move(232, 10)

    def calculation(self):
        self.second_value.setText(str(eval(self.first_value.text())))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Evaluator()
    ex.show()
    sys.exit(app.exec())
