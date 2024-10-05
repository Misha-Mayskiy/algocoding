import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QPlainTextEdit, QSpinBox, \
    QHBoxLayout


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Цены на блюда
        self.prices = {
            "Чизбургер": 10,
            "Гамбургер": 20,
            "Кока-кола": 15,
            "Наггетсы": 30
        }

        # Инициализируем списки для чекбоксов и спинбоксов
        self.checkboxes = []
        self.inputs = []

        self.init_ui()

    def init_ui(self):
        # Создаем основное вертикальное расположение элементов
        layout = QVBoxLayout()

        # Меню для заказа с количеством порций
        menu_items = ["Чизбургер", "Гамбургер", "Кока-кола", "Наггетсы"]

        for item in menu_items:
            # Горизонтальный layout для каждого пункта меню
            item_layout = QHBoxLayout()

            # Чекбокс для выбора блюда
            checkbox = QCheckBox(item)
            self.checkboxes.append(checkbox)

            # Спинбокс для указания количества порций
            spinbox = QSpinBox()
            spinbox.setMinimum(0)
            spinbox.setValue(0)
            spinbox.setEnabled(False)
            self.inputs.append(spinbox)

            # Активируем спинбокс при выборе блюда
            checkbox.stateChanged.connect(lambda state, spinbox=spinbox: spinbox.setEnabled(state == 2))

            # Добавляем чекбокс и спинбокс в горизонтальный layout
            item_layout.addWidget(checkbox)
            item_layout.addWidget(spinbox)

            # Добавляем в основной layout
            layout.addLayout(item_layout)

        # Кнопка для подтверждения заказа
        self.orderButton = QPushButton("Заказать")
        self.orderButton.clicked.connect(self.show_order)
        layout.addWidget(self.orderButton)

        # Поле для отображения итогового заказа
        self.order = QPlainTextEdit()
        self.order.setReadOnly(True)
        layout.addWidget(self.order)

        # Устанавливаем основной layout
        self.setLayout(layout)
        self.setWindowTitle('Заказ в Макдональдсе 2')

    def show_order(self):
        # Формируем текст заказа и считаем общую стоимость
        order_text = "Ваш заказ\n\n"
        total_price = 0

        for checkbox, spinbox in zip(self.checkboxes, self.inputs):
            if checkbox.isChecked():
                item_name = checkbox.text()
                quantity = spinbox.value()
                item_price = self.prices[item_name] * quantity
                total_price += item_price

                # Добавляем информацию о выбранном блюде
                order_text += f"{item_name}-----{quantity}-----{item_price}\n"

        order_text += f"\nИтого: {total_price}"

        # Выводим заказ в виджет
        self.order.setPlainText(order_text)


# Основная функция
def main():
    app = QApplication(sys.argv)
    window = MyWidget()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
