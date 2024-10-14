import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QDoubleSpinBox,
    QPlainTextEdit,
    QPushButton,
    QStatusBar
)


class AntiPlagiarism(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()
        self.initUI()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(400, 300)
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)

        # SpinBox для порога
        self.alert_value = QDoubleSpinBox(self.centralwidget)
        self.alert_value.setDecimals(2)
        self.alert_value.setRange(0.0, 100.0)
        self.layout.addWidget(self.alert_value)

        # TextEdit для первого текста
        self.text1 = QPlainTextEdit(self.centralwidget)
        self.layout.addWidget(self.text1)

        # TextEdit для второго текста
        self.text2 = QPlainTextEdit(self.centralwidget)
        self.layout.addWidget(self.text2)

        # Кнопка для проверки
        self.checkBtn = QPushButton("Проверить", self.centralwidget)
        self.layout.addWidget(self.checkBtn)

        # Статус бар для вывода результата
        self.statusbar = QStatusBar(self)
        self.setStatusBar(self.statusbar)

        # Назначаем имя для окна
        self.setWindowTitle("Проверка на антиплагиат")

    def initUI(self):
        self.checkBtn.clicked.connect(self.sravnit)

    def sravnit(self):
        # Получаем текст из полей без начальных и конечных пробелов
        text1_raw = self.text1.toPlainText().strip()
        text2_raw = self.text2.toPlainText().strip()

        # Заменяем '\\n' на '\n' для корректного разбиения на строки
        text1_processed = text1_raw.replace('\\n', '\n')
        text2_processed = text2_raw.replace('\\n', '\n')

        # Если текст пустой после замены, считаем, что он содержит одну пустую строку
        if text1_processed == '':
            text1 = ['']
        else:
            text1 = text1_processed.splitlines()

        if text2_processed == '':
            text2 = ['']
        else:
            text2 = text2_processed.splitlines()

        # Получаем уникальные строки
        unique_lines1 = set(text1)
        unique_lines2 = set(text2)

        # Находим общие строки
        common_lines = unique_lines1.intersection(unique_lines2)

        # Находим все уникальные строки
        total_unique_lines = unique_lines1.union(unique_lines2)

        # Рассчитываем процент схожести
        if total_unique_lines:
            similarity_percentage = len(common_lines) / len(total_unique_lines) * 100
        else:
            similarity_percentage = 0

        # Получаем пороговое значение
        alert_value = self.alert_value.value()

        # Проверяем порог и выводим сообщение
        if alert_value > 0:
            if similarity_percentage >= alert_value:
                self.statusbar.showMessage(f"Тексты похожи на {similarity_percentage:.2f}%, плагиат")
            else:
                self.statusbar.showMessage(f"Тексты похожи на {similarity_percentage:.2f}%, не плагиат")
        else:
            self.statusbar.showMessage("Введите порог сравнения")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AntiPlagiarism()
    ex.show()
    sys.exit(app.exec())
