import string
import sys

from PyQt6.QtWidgets import QLineEdit, QPushButton
from PyQt6.QtWidgets import QWidget, QApplication


class MorseCode(QWidget):
    def __init__(self):
        super(MorseCode, self).__init__()

        self.setWindowTitle('Азбука Морзе 2')
        self.setGeometry(300, 300, 700, 100)
        # В этот словарь мы поставим каждому ключу объект класса QPushButton
        self.alphabet_buttons = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
                                 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..',
                                 'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                                 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...',
                                 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
                                 'y': '-.--', 'z': '--..'}
        # Это словарь нужен чтобы переводить буквы в код
        self.alphabet = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..',
                         'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..',
                         'j': '.---', 'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.',
                         'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...',
                         't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
                         'y': '-.--', 'z': '--..'}
        self.initUI()

    def initUI(self):
        i = 0
        for k, v in self.alphabet_buttons.items():
            self.alphabet_buttons[k] = QPushButton(self)
            self.alphabet_buttons[k].move(20 + i * 20, 20)
            self.alphabet_buttons[k].resize(20, 20)
            self.alphabet_buttons[k].setText(string.ascii_lowercase[i])
            self.alphabet_buttons[k].clicked.connect(self.goCode)
            i += 1

        self.result = QLineEdit(self)
        self.result.move(20, 60)
        self.result.resize(660, 30)
        self.result.setText("")

    def goCode(self):
        self.result.setText(self.result.text() + self.alphabet[str(self.sender().text())])


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MorseCode()
    ex.show()
    sys.exit(app.exec())
