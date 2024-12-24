import sys

from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, \
    QButtonGroup


class TicTacToe(QWidget):
    def __init__(self):
        super().__init__()

        # Инициализация основных переменных
        self.current_player = 'X'
        self.game_over = False
        self.button_grid = [[None for _ in range(3)] for _ in range(3)]

        # Создание элементов интерфейса
        self.result = QLabel("", self)
        self.x_radio = QRadioButton('X', self)
        self.o_radio = QRadioButton('O', self)
        self.new_game_button = QPushButton('Новая игра', self)

        self.x_radio.setChecked(True)  # По умолчанию первый игрок X
        self.new_game_button.clicked.connect(self.new_game)

        # Настройка группировки радиокнопок
        radio_layout = QHBoxLayout()
        radio_layout.addWidget(QLabel("Первый игрок: "))
        radio_layout.addWidget(self.x_radio)
        radio_layout.addWidget(self.o_radio)

        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.x_radio)
        self.radio_group.addButton(self.o_radio)

        self.x_radio.toggled.connect(self.radio_changed)

        # Настройка сетки для игрового поля
        grid_layout = QVBoxLayout()

        for row in range(3):
            row_layout = QHBoxLayout()
            for col in range(3):
                button = QPushButton('')
                button.setFixedSize(100, 100)
                button.clicked.connect(lambda checked, r=row, c=col: self.button_clicked(r, c))
                self.button_grid[row][col] = button
                row_layout.addWidget(button)
            grid_layout.addLayout(row_layout)

        # Главный макет приложения
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.result)
        main_layout.addLayout(radio_layout)
        main_layout.addLayout(grid_layout)
        main_layout.addWidget(self.new_game_button)

        self.setLayout(main_layout)
        self.setWindowTitle('Крестики-нолики')
        self.show()

    # Обработчик нажатий на кнопки игрового поля
    def button_clicked(self, row, col):
        if not self.game_over and self.button_grid[row][col].text() == '':
            self.button_grid[row][col].setText(self.current_player)
            if self.check_win():
                self.result.setText(f"Выиграл {self.current_player}!")
                self.game_over = True
                self.disable_buttons()
            elif self.check_draw():
                self.result.setText("Ничья!")
                self.game_over = True
            else:
                self.switch_player()

    # Переключение между игроками
    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    # Проверка на победу
    def check_win(self):
        for i in range(3):
            # Проверка строк
            if self.button_grid[i][0].text() == self.button_grid[i][1].text() == self.button_grid[i][2].text() != '':
                return True
            # Проверка колонок
            if self.button_grid[0][i].text() == self.button_grid[1][i].text() == self.button_grid[2][i].text() != '':
                return True
        # Проверка диагоналей
        if self.button_grid[0][0].text() == self.button_grid[1][1].text() == self.button_grid[2][2].text() != '':
            return True
        if self.button_grid[0][2].text() == self.button_grid[1][1].text() == self.button_grid[2][0].text() != '':
            return True
        return False

    # Проверка на ничью
    def check_draw(self):
        for row in self.button_grid:
            for button in row:
                if button.text() == '':
                    return False
        return True

    # Отключение кнопок после окончания игры
    def disable_buttons(self):
        for row in self.button_grid:
            for button in row:
                button.setEnabled(False)

    # Начало новой игры
    def new_game(self):
        self.game_over = False
        self.current_player = 'X' if self.x_radio.isChecked() else 'O'
        self.result.setText('')
        for row in self.button_grid:
            for button in row:
                button.setEnabled(True)
                button.setText('')

    # Смена игрока при изменении радиокнопок
    def radio_changed(self):
        self.new_game()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TicTacToe()
    sys.exit(app.exec())
