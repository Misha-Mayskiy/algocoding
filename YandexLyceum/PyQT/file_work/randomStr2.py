import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout


class RandomString(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Случайная строка из файла')

        self.text_field = QTextEdit(self)
        self.text_field.setReadOnly(True)

        self.button = QPushButton('Получить случайную строку', self)
        self.button.clicked.connect(self.display_random_line)

        layout = QVBoxLayout()
        layout.addWidget(self.text_field)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.resize(400, 300)

    def display_random_line(self):
        try:
            with open('lines.txt', encoding='utf-8') as file:
                lines = file.readlines()
            if lines:
                random_line = random.choice(lines).strip()
                self.text_field.setPlainText(random_line)
            else:
                self.text_field.clear()
        except FileNotFoundError:
            self.text_field.setPlainText('Файл lines.txt не найден.')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RandomString()
    window.show()
    sys.exit(app.exec())