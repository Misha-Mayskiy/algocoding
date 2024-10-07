import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QRadioButton, QPushButton, QButtonGroup


class FlagMaker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Текстовый флаг")
        self.setFixedSize(300, 200)  # Фиксируем размер окна

        # Основной вертикальный layout
        layout = QVBoxLayout()

        # Группы кнопок для выбора цветов
        self.color_group_1 = QButtonGroup(self)
        self.color_group_2 = QButtonGroup(self)
        self.color_group_3 = QButtonGroup(self)

        # Первая группа (верхняя полоса флага)
        self.add_color_buttons(layout, self.color_group_1, "Верхняя полоса")

        # Вторая группа (средняя полоса флага)
        self.add_color_buttons(layout, self.color_group_2, "Средняя полоса")

        # Третья группа (нижняя полоса флага)
        self.add_color_buttons(layout, self.color_group_3, "Нижняя полоса")

        # Кнопка для создания флага
        self.make_flag = QPushButton("Сделать флаг", self)
        self.make_flag.clicked.connect(self.generate_flag)
        layout.addWidget(self.make_flag)

        # Элемент для отображения текста результата
        self.result = QLabel("", self)
        self.result.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.result)

        # Устанавливаем layout
        self.setLayout(layout)

    def add_color_buttons(self, layout, button_group, label_text):
        """Добавляет радио-кнопки для выбора цветов и добавляет их в группу"""
        label = QLabel(label_text, self)
        layout.addWidget(label)

        blue_button = QRadioButton("Синий", self)
        red_button = QRadioButton("Красный", self)
        green_button = QRadioButton("Зелёный", self)

        button_group.addButton(blue_button)
        button_group.addButton(red_button)
        button_group.addButton(green_button)

        # Добавляем радио-кнопки в layout
        layout.addWidget(blue_button)
        layout.addWidget(red_button)
        layout.addWidget(green_button)

    def generate_flag(self):
        """Генерирует текстовый флаг на основе выбранных цветов"""
        color1 = self.get_selected_color(self.color_group_1)
        color2 = self.get_selected_color(self.color_group_2)
        color3 = self.get_selected_color(self.color_group_3)

        if color1 and color2 and color3:
            flag_text = f"Цвета: {color1}, {color2} и {color3}"
            self.result.setText(flag_text)
        else:
            self.result.setText("Пожалуйста, выберите цвет для каждой полосы.")

    def get_selected_color(self, button_group):
        """Возвращает текст выбранной радио-кнопки из группы"""
        selected_button = button_group.checkedButton()
        if selected_button:
            return selected_button.text()
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlagMaker()
    window.show()
    sys.exit(app.exec())
