import sys

from PyQt6.QtWidgets import *


class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("AntiPlagiarism")
        self.setGeometry(200, 200, 400, 300)

        self.init_ui()

    def init_ui(self):
        # Основной центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Порог срабатывания антиплагиата (QDoubleSpinBox)
        self.alert_value = QDoubleSpinBox()
        self.alert_value.setRange(0, 100)
        self.alert_value.setValue(50.0)  # Установим начальный порог 50%
        self.alert_value.setSuffix("%")  # Процентное значение
        layout.addWidget(self.alert_value)

        # Поля для ввода двух текстов (QPlainTextEdit)
        self.text1 = QPlainTextEdit()
        self.text1.setPlaceholderText("Введите первый текст")
        layout.addWidget(self.text1)

        self.text2 = QPlainTextEdit()
        self.text2.setPlaceholderText("Введите второй текст")
        layout.addWidget(self.text2)

        # Кнопка для проверки (QPushButton)
        self.checkBtn = QPushButton("Проверить")
        self.checkBtn.clicked.connect(self.check_plagiarism)
        layout.addWidget(self.checkBtn)

        # Установка layout на центральный виджет
        central_widget.setLayout(layout)

        # Status bar для вывода результата
        self.statusbar = self.statusBar()

    def check_plagiarism(self):
        # Получаем тексты из полей ввода
        text1_lines = set(self.text1.toPlainText().splitlines())
        text2_lines = set(self.text2.toPlainText().splitlines())

        # Общие уникальные строки
        common_lines = text1_lines.intersection(text2_lines)

        # Процент схожести
        if len(text1_lines.union(text2_lines)) > 0:
            similarity = (len(common_lines) / len(text1_lines.union(text2_lines))) * 100
        else:
            similarity = 0.0

        # Получаем порог для антиплагиата
        threshold = self.alert_value.value()

        # Формируем сообщение
        result_message = f"Тексты похожи на {similarity:.2f}%"
        if similarity >= threshold:
            result_message += ", плагиат"
        else:
            result_message += ", не плагиат"

        # Выводим результат в status bar
        self.statusbar.showMessage(result_message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiPlagiarism()
    window.show()
    sys.exit(app.exec())
