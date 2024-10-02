import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout


class Arifmometr(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Арифмометр')
        self.setGeometry(100, 100, 400, 300)

        self.first_value = QLineEdit(self)
        self.second_value = QLineEdit(self)

        self.multiply_button = QPushButton("*", self)
        self.multiply_button.clicked.connect(self.calculate)
        self.substract_button = QPushButton("-", self)
        self.substract_button.clicked.connect(self.calculate)
        self.add_button = QPushButton("+", self)
        self.add_button.clicked.connect(self.calculate)

        self.result = QLineEdit(self)
        self.result.setReadOnly(True)

        layout = QVBoxLayout()
        layout.addWidget(self.first_value)
        layout.addWidget(self.multiply_button)
        layout.addWidget(self.substract_button)
        layout.addWidget(self.add_button)
        layout.addWidget(self.second_value)
        layout.addWidget(self.result)
        self.setLayout(layout)

    def calculate(self):
        global result
        sender = self.sender()

        if sender == self.multiply_button:
            result = float(self.first_value.text()) * float(self.second_value.text())
        elif sender == self.substract_button:
            result = float(self.first_value.text()) - float(self.second_value.text())
        elif sender == self.add_button:
            result = float(self.first_value.text()) + float(self.second_value.text())

        self.result.setText(str(int(result)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_form = Arifmometr()
    my_form.show()
    sys.exit(app.exec())
