import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QGridLayout, QVBoxLayout
)


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Калькулятор")
        self.setFixedSize(300, 400)

        # Инициализация состояния калькулятора
        self.reset_all()

        # Создание интерфейса
        self.create_ui()

    def reset_all(self):
        """Сброс всех операций и состояний калькулятора."""
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.reset_next = False
        self.error = False

    def create_ui(self):
        """Создание и размещение всех компонентов калькулятора."""

        # Создание вертикального основного лэйаута
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Дополнительное поле ввода (верхнее)
        self.secondary_label = QLabel("")
        self.secondary_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.secondary_label.setFont(QFont("Arial", 12))
        self.secondary_label.setStyleSheet("background-color: lightgray;")
        self.secondary_label.setFixedHeight(30)
        main_layout.addWidget(self.secondary_label)

        # Основное поле ввода (нижнее)
        self.main_label = QLabel(self.current)
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_label.setFont(QFont("Arial", 24))
        self.main_label.setStyleSheet("background-color: white;")
        self.main_label.setFixedHeight(50)
        main_layout.addWidget(self.main_label)

        # Создание сетки для кнопок
        button_layout = QGridLayout()
        main_layout.addLayout(button_layout)

        # Определение кнопок
        self.number_buttons = [QPushButton(str(i)) for i in range(10)]
        self.clear_button = QPushButton("C")
        self.clear_entry_button = QPushButton("CE")
        self.divide_button = QPushButton("/")
        self.multiply_button = QPushButton("*")
        self.substract_button = QPushButton("-")
        self.add_button = QPushButton("+")
        self.float_point_button = QPushButton(".")
        self.plus_minus_button = QPushButton("±")
        self.equals_button = QPushButton("=")

        # Настройка стиля кнопок
        for button in self.number_buttons + [
            self.clear_button, self.clear_entry_button,
            self.divide_button, self.multiply_button,
            self.substract_button, self.add_button,
            self.float_point_button, self.plus_minus_button,
            self.equals_button
        ]:
            button.setFixedSize(60, 40)
            button.setFont(QFont("Arial", 14))

        # Расположение кнопок на сетке
        # Первая строка
        button_layout.addWidget(self.clear_button, 0, 0)
        button_layout.addWidget(self.clear_entry_button, 0, 1)
        button_layout.addWidget(self.divide_button, 0, 2)
        button_layout.addWidget(self.multiply_button, 0, 3)

        # Вторая строка
        button_layout.addWidget(self.number_buttons[7], 1, 0)
        button_layout.addWidget(self.number_buttons[8], 1, 1)
        button_layout.addWidget(self.number_buttons[9], 1, 2)
        button_layout.addWidget(self.substract_button, 1, 3)

        # Третья строка
        button_layout.addWidget(self.number_buttons[4], 2, 0)
        button_layout.addWidget(self.number_buttons[5], 2, 1)
        button_layout.addWidget(self.number_buttons[6], 2, 2)
        button_layout.addWidget(self.add_button, 2, 3)

        # Четвертая строка
        button_layout.addWidget(self.number_buttons[1], 3, 0)
        button_layout.addWidget(self.number_buttons[2], 3, 1)
        button_layout.addWidget(self.number_buttons[3], 3, 2)
        button_layout.addWidget(self.equals_button, 3, 3, 2, 1)  # Рядом с равенством будут две строки

        # Пятая строка
        button_layout.addWidget(self.plus_minus_button, 4, 0)
        button_layout.addWidget(self.number_buttons[0], 4, 1)
        button_layout.addWidget(self.float_point_button, 4, 2)

        # Подключение сигналов к слотам
        for i, button in enumerate(self.number_buttons):
            button.clicked.connect(lambda checked, x=i: self.input_number(x))
        self.clear_button.clicked.connect(self.clear_all)
        self.clear_entry_button.clicked.connect(self.clear_entry)
        self.divide_button.clicked.connect(lambda: self.set_operator("/"))
        self.multiply_button.clicked.connect(lambda: self.set_operator("*"))
        self.substract_button.clicked.connect(lambda: self.set_operator("-"))
        self.add_button.clicked.connect(lambda: self.set_operator("+"))
        self.float_point_button.clicked.connect(self.input_dot)
        self.plus_minus_button.clicked.connect(self.toggle_sign)
        self.equals_button.clicked.connect(self.calculate)

    def input_number(self, num):
        """Обработка ввода цифры."""
        if self.error:
            self.reset_all()
        if self.reset_next:
            self.current = ""
            self.reset_next = False
        if self.current == "0":
            self.current = str(num)
        else:
            self.current += str(num)
        self.update_display()

    def input_dot(self):
        """Обработка ввода точки."""
        pass

    def toggle_sign(self):
        """Смена знака текущего числа."""
        pass

    def set_operator(self, op):
        """Установка арифметического оператора."""
        if self.error:
            return
        if self.operator and not self.reset_next:
            self.calculate()
        self.previous = self.current
        self.operator = op
        self.secondary_label.setText(f"{self.format_number(self.previous)} {self.operator}")
        self.reset_next = True

    def calculate(self):
        """Выполнение арифметической операции."""
        if not self.operator:
            return
        try:
            num1 = float(self.previous)
            num2 = float(self.current)
            result = 0
            if self.operator == "+":
                result = num1 + num2
            elif self.operator == "-":
                result = num1 - num2
            elif self.operator == "*":
                result = num1 * num2
            elif self.operator == "/":
                if num2 == 0:
                    raise ZeroDivisionError
                result = num1 / num2

            # Удаление .0 если число целое
            if result == int(result):
                result = int(result)
                self.current = str(result)
            else:
                self.current = str(result)

            self.secondary_label.setText(
                f"{self.format_number(self.previous)} {self.operator} {self.format_number(self.current)}")
            self.main_label.setText(self.format_number(self.current, main=True))
            self.operator = ""
            self.reset_next = True
        except ZeroDivisionError:
            self.main_label.setText("ОШИБКА")
            self.secondary_label.setText("")
            self.error = True
        except Exception:
            self.main_label.setText("ОШИБКА")
            self.secondary_label.setText("")
            self.error = True

    def clear_all(self):
        """Очистка всех вводов и состояний."""
        self.reset_all()
        self.secondary_label.setText("")
        self.update_display()

    def clear_entry(self):
        """Очистка текущего ввода."""
        if self.error:
            self.clear_all()
            return
        self.current = "0"
        self.update_display()

    def update_display(self):
        """Обновление отображения на экране калькулятора."""
        formatted = self.format_number(self.current, main=True)
        self.main_label.setText(formatted)
        if self.operator:
            self.secondary_label.setText(f"{self.format_number(self.previous)} {self.operator}")
        else:
            self.secondary_label.setText("")

    def format_number(self, num_str, main=False):
        """
        Форматирование числа с учетом ограничений по длине.
        :param num_str: Число в виде строки.
        :param main: Флаг для основного поля (ограничение 11 символов).
        :return: Отформатированная строка.
        """
        try:
            num = float(num_str)
            # Удаление .0 если число целое
            if num == int(num):
                num = int(num)
            if main:
                display = str(num)
                if len(display) > 11:
                    display = f"{num:.2e}"
            else:
                display = str(num)
                if len(str(num).replace('-', '').replace('.', '')) > 30:
                    display = f"{num:.2e}"
            return display
        except Exception:
            return "ОШИБКА"


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec())
