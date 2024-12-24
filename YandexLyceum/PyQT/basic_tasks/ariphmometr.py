import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout


class Arifmometr(QWidget):
    def __init__(self):
        super().__init__()

        # Создание элементов интерфейса
        self.first_value = QLineEdit(self)
        self.second_value = QLineEdit(self)
        self.result = QLineEdit(self)
        self.result.setReadOnly(True)  # Запрещаем редактирование поля результата

        self.add_button = QPushButton('+', self)
        self.substract_button = QPushButton('-', self)
        self.multiply_button = QPushButton('*', self)

        # Установка значений по умолчанию
        self.first_value.setText('0')
        self.second_value.setText('0')
        self.result.setText('0')

        # Настройка компоновки интерфейса
        layout = QVBoxLayout()

        form_layout = QFormLayout()
        form_layout.addRow('Первое число:', self.first_value)
        form_layout.addRow('Второе число:', self.second_value)
        form_layout.addRow('Результат:', self.result)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.substract_button)
        button_layout.addWidget(self.multiply_button)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # Привязка сигналов к кнопкам
        self.add_button.clicked.connect(self.add)
        self.substract_button.clicked.connect(self.substract)
        self.multiply_button.clicked.connect(self.multiply)

        self.setWindowTitle('Арифмометр')

    def add(self):
        try:
            first_value = int(self.first_value.text())
            second_value = int(self.second_value.text())
            result = first_value + second_value
            self.result.setText(str(result))
        except ValueError:
            self.result.setText('Ошибка')

    def substract(self):
        try:
            first_value = int(self.first_value.text())
            second_value = int(self.second_value.text())
            result = first_value - second_value
            self.result.setText(str(result))
        except ValueError:
            self.result.setText('Ошибка')

    def multiply(self):
        try:
            first_value = int(self.first_value.text())
            second_value = int(self.second_value.text())
            result = first_value * second_value
            self.result.setText(str(result))
        except ValueError:
            self.result.setText('Ошибка')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Arifmometr()
    window.show()
    sys.exit(app.exec())
