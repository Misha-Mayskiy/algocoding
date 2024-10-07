import sys

from PyQt6.QtWidgets import *


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Создаем основное вертикальное расположение элементов
        layout = QVBoxLayout()

        # Словарь для хранения цен на блюда
        self.prices = {
            "Чизбургер": 10,
            "Гамбургер": 20,
            "Кока-кола": 15,
            "Наггетсы": 30
        }

        # Создаем чекбоксы и поля для ввода
        self.checkboxes = []
        self.inputs = []

        for item in self.prices.keys():
            checkbox = QCheckBox(item)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

            input_field = QLineEdit("1")  # Устанавливаем по умолчанию количество 1
            input_field.setEnabled(False)  # Поле ввода отключено, пока чекбокс не отмечен
            self.inputs.append(input_field)
            layout.addWidget(input_field)

            # Подключаем сигнал для активации поля ввода
            checkbox.stateChanged.connect(lambda state, index=len(self.checkboxes) - 1: self.toggle_input(index))

        # Создаем кнопку заказа
        self.orderButton = QPushButton("Заказать")
        self.orderButton.clicked.connect(self.show_order)
        layout.addWidget(self.orderButton)

        # Создаем виджет для отображения результата
        self.order = QPlainTextEdit()
        self.order.setReadOnly(True)
        layout.addWidget(self.order)

        # Устанавливаем основной layout в виджет
        self.setLayout(layout)
        self.setWindowTitle('Заказ в Макдональдсе')

    def toggle_input(self, index):
        # Активируем или деактивируем поле ввода в зависимости от состояния чекбокса
        self.inputs[index].setEnabled(self.checkboxes[index].isChecked())
        if not self.checkboxes[index].isChecked():
            self.inputs[index].setText("1")  # Сбрасываем количество на 1, если чекбокс не отмечен

    def show_order(self):
        # Формируем текст заказа
        order = "Ваш заказ\n\n"
        total_cost = 0

        for checkbox, input_field in zip(self.checkboxes, self.inputs):
            if checkbox.isChecked():
                item_name = checkbox.text()
                quantity = int(input_field.text()) if input_field.text().isdigit() else 1
                item_cost = self.prices[item_name] * quantity
                total_cost += item_cost
                order += f"{item_name}-----{quantity}-----{item_cost}\n"

        order += f"\nИтого: {total_cost}"

        # Выводим заказ в виджет результата
        self.order.setPlainText(order)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())
