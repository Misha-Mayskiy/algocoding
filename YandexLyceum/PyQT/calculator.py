import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        # Основные поля ввода
        self.main_label = QLineEdit(self)
        self.main_label.setReadOnly(True)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_label.setFixedHeight(50)
        self.main_label.setText('0')  # Инициализация с "0"

        self.secondary_label = QLineEdit(self)
        self.secondary_label.setReadOnly(True)
        self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.secondary_label.setFixedHeight(30)

        # Кнопки чисел
        self.number_buttons = [QPushButton(str(i), self) for i in range(10)]
        for button in self.number_buttons:
            button.clicked.connect(self.number_clicked)

        # Кнопки операций
        self.clear_button = QPushButton('C', self)
        self.clear_entry_button = QPushButton('CE', self)
        self.divide_button = QPushButton('/', self)
        self.multiply_button = QPushButton('*', self)
        self.substract_button = QPushButton('-', self)
        self.add_button = QPushButton('+', self)
        self.float_point_button = QPushButton('.', self)
        self.plus_minus_button = QPushButton('±', self)
        self.equals_button = QPushButton('=', self)

        # Подключение сигналов
        self.clear_button.clicked.connect(self.clear)
        self.clear_entry_button.clicked.connect(self.clear_entry)
        self.divide_button.clicked.connect(lambda: self.operation('/'))
        self.multiply_button.clicked.connect(lambda: self.operation('*'))
        self.substract_button.clicked.connect(lambda: self.operation('-'))
        self.add_button.clicked.connect(lambda: self.operation('+'))
        self.float_point_button.clicked.connect(self.add_float_point)
        self.plus_minus_button.clicked.connect(self.toggle_sign)
        self.equals_button.clicked.connect(self.calculate)

        # Настройка компоновки
        layout = QVBoxLayout()
        layout.addWidget(self.secondary_label)
        layout.addWidget(self.main_label)

        button_layout = QVBoxLayout()

        # Кнопки чисел
        for i in range(3):
            row_layout = QHBoxLayout()
            for j in range(3):
                row_layout.addWidget(self.number_buttons[i * 3 + j + 1])
            button_layout.addLayout(row_layout)

        # Последний ряд с 0, точкой и кнопкой смены знака
        last_row_layout = QHBoxLayout()
        last_row_layout.addWidget(self.number_buttons[0])
        last_row_layout.addWidget(self.float_point_button)
        last_row_layout.addWidget(self.plus_minus_button)
        button_layout.addLayout(last_row_layout)

        # Кнопки операций
        operations_layout = QVBoxLayout()
        operations_layout.addWidget(self.clear_button)
        operations_layout.addWidget(self.clear_entry_button)
        operations_layout.addWidget(self.divide_button)
        operations_layout.addWidget(self.multiply_button)
        operations_layout.addWidget(self.substract_button)
        operations_layout.addWidget(self.add_button)
        operations_layout.addWidget(self.equals_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(button_layout)
        main_layout.addLayout(operations_layout)

        layout.addLayout(main_layout)
        self.setLayout(layout)

        self.setWindowTitle('Калькулятор')
        self.setFixedSize(300, 400)

        # Переменные для хранения состояния
        self.first_operand = None
        self.second_operand = None
        self.current_operation = None
        self.clear_secondary_label()

    def number_clicked(self):
        button = self.sender()
        number = button.text()
        if self.main_label.text() in ['0', 'ОШИБКА']:
            self.main_label.setText(number)
        else:
            self.main_label.setText(self.main_label.text() + number)

    def operation(self, operator):
        if self.current_operation:
            self.calculate()
        self.first_operand = self.get_number(self.main_label.text())
        self.current_operation = operator
        self.secondary_label.setText(f"{self.first_operand} {operator} ")

        self.main_label.setText('0')

    def calculate(self):
        if self.current_operation is None:
            return

        self.second_operand = self.get_number(self.main_label.text())
        try:
            if self.current_operation == '+':
                result = self.first_operand + self.second_operand
            elif self.current_operation == '-':
                result = self.first_operand - self.second_operand
            elif self.current_operation == '*':
                result = self.first_operand * self.second_operand
            elif self.current_operation == '/':
                if self.second_operand == 0:
                    raise ZeroDivisionError
                result = self.first_operand / self.second_operand
        except ZeroDivisionError:
            self.main_label.setText('ОШИБКА')
            self.clear_secondary_label()
            return

        self.main_label.setText(self.format_result(result))
        self.clear_secondary_label()
        self.current_operation = None

    def clear(self):
        self.main_label.setText('0')
        self.clear_secondary_label()
        self.first_operand = None
        self.second_operand = None
        self.current_operation = None

    def clear_entry(self):
        # Очищаем только главное поле
        self.main_label.setText('0')  # Только очищаем main_label, не трогаем secondary_label

    def add_float_point(self):
        if '.' not in self.main_label.text():
            self.main_label.setText(self.main_label.text() + '.')

    def toggle_sign(self):
        current_value = self.main_label.text()
        # Преобразуем строку в число, чтобы точно определить, является ли оно нулем
        if current_value == "ОШИБКА":
            return
        numeric_value = float(current_value)
        if numeric_value == 0:
            return
        self.main_label.setText(str(-numeric_value))

    def get_number(self, text):
        try:
            return float(text)
        except ValueError:
            return 0.0

    def format_result(self, result):
        if result % 1 == 0:
            return "{:.0f}".format(result)  # Выводим целые числа без знаков после запятой
        elif abs(result) >= 1e12:  # Если число большое, используем научную нотацию
            return "{:.2e}".format(result)
        return "{:.10g}".format(result)

    def clear_secondary_label(self):
        self.secondary_label.setText('')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec())
