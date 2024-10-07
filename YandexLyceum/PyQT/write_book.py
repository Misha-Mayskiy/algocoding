import sys
from PyQt6.QtWidgets import *


class WidgetArt(QWidget):
    def __init__(self, matrix):
        super().__init__()

        # Настройка интерфейса
        self.setWindowTitle("Widget Art")
        self.setFixedSize(400, 400)

        # Создание сеточного layout для отображения матрицы
        self.widgetArt = QGridLayout()
        self.setLayout(self.widgetArt)

        # Заполнение сетки кнопками в зависимости от матрицы
        self.create_buttons(matrix)

    def create_buttons(self, matrix):
        for row_idx, row in enumerate(matrix):
            for col_idx, value in enumerate(row):
                # Создаем кнопку с текстом '*' если значение 1, или пустую если 0
                btn_text = '*' if value == 1 else ''
                button = QPushButton(btn_text)
                button.setFixedSize(30, 30)  # Фиксированный размер кнопок
                # Добавляем кнопку в сетку по координатам
                self.widgetArt.addWidget(button, row_idx, col_idx)
