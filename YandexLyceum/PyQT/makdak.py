import sys

from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QPushButton, QPlainTextEdit


class MacOrder(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        # Создаем основное вертикальное расположение элементов
        layout = QVBoxLayout()

        # Создаем чекбоксы для меню
        self.menu_checkboxes = [
            QCheckBox("Чизбургер"),
            QCheckBox("Гамбургер"),
            QCheckBox("Кока-кола"),
            QCheckBox("Наггетсы")
        ]

        # Добавляем чекбоксы в основной layout
        for checkbox in self.menu_checkboxes:
            layout.addWidget(checkbox)

        # Создаем кнопку заказа
        self.order_btn = QPushButton("Заказать")
        self.order_btn.clicked.connect(self.show_order)
        layout.addWidget(self.order_btn)

        # Создаем виджет для отображения результата
        self.result = QPlainTextEdit()
        self.result.setReadOnly(True)
        layout.addWidget(self.result)

        # Устанавливаем основной layout в виджет
        self.setLayout(layout)
        self.setWindowTitle('Заказ в Макдональдсе')

    def show_order(self):
        # Формируем текст заказа
        order = "Ваш заказ:\n\n"
        selected_items = [checkbox.text() for checkbox in self.menu_checkboxes if checkbox.isChecked()]

        if selected_items:
            order += "\n".join(selected_items)
        else:
            order += "Вы ничего не выбрали."

        # Выводим заказ в виджет результата
        self.result.setPlainText(order)


# Основная функция
def main():
    app = QApplication(sys.argv)
    window = MacOrder()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
