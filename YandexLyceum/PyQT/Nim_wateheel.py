import random
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout


class NimStrikesBack(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация начальных значений X, Y, Z
        self.X = random.randint(10, 30)
        self.Y = random.randint(1, 10)
        self.Z = random.randint(-10, -1)
        self.moves_left = 10

        # Создание виджетов
        self.initUI()

    def initUI(self):
        # Главная надпись с текущим значением X
        self.label = QLabel(f'Текущее число: {self.X}', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Надпись с количеством оставшихся ходов
        self.moves_label = QLabel(f'Осталось ходов: {self.moves_left}', self)
        self.moves_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Кнопки для изменения X
        self.btnp = QPushButton(str(self.Y), self)
        self.btnp.clicked.connect(self.increase)

        self.btnm = QPushButton(str(self.Z), self)
        self.btnm.clicked.connect(self.decrease)

        # Результат
        self.result_label = QLabel('', self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Макет
        vbox = QVBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.moves_label)
        vbox.addWidget(self.btnp)
        vbox.addWidget(self.btnm)
        vbox.addWidget(self.result_label)

        self.setLayout(vbox)

        # Настройки окна
        self.setWindowTitle('Ним наносит ответный удар')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def increase(self):
        if self.moves_left > 0:
            self.X += self.Y
            self.update_game()

    def decrease(self):
        if self.moves_left > 0:
            self.X += self.Z
            self.update_game()

    def update_game(self):
        self.moves_left -= 1
        self.label.setText(f'Текущее число: {self.X}')
        self.moves_label.setText(f'Осталось ходов: {self.moves_left}')
        self.result_label.setText('')

        if self.X == 0:
            self.result_label.setText('Вы победили, начинаем новую игру')
            self.end_game()
        elif self.moves_left == 0 and self.X != 0:
            self.result_label.setText('Вы проиграли, начинаем новую игру')
            self.end_game()

    def end_game(self):
        self.X = random.randint(10, 30)
        self.Y = random.randint(1, 10)
        self.Z = random.randint(-10, -1)
        self.moves_left = 10
        self.label.setText(f'Текущее число: {self.X}')
        self.moves_label.setText(f'Осталось ходов: {self.moves_left}')
        self.btnp.setText(str(self.Y))
        self.btnm.setText(str(self.Z))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = NimStrikesBack()
    sys.exit(app.exec())
