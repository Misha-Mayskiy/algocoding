import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton,
                             QLabel, QVBoxLayout, QWidget, QStatusBar)



class FileStat(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Файловая статистика')

        # Widgets
        self.filenameEdit = QLineEdit(self)
        self.button = QPushButton('Рассчитать', self)
        self.maxEdit = QLineEdit(self)
        self.minEdit = QLineEdit(self)
        self.avgEdit = QLineEdit(self)

        # Read-only output fields
        self.maxEdit.setReadOnly(True)
        self.minEdit.setReadOnly(True)
        self.avgEdit.setReadOnly(True)

        # Labels
        filenameLabel = QLabel('Имя файла:', self)
        maxLabel = QLabel('Максимальное значение:', self)
        minLabel = QLabel('Минимальное значение:', self)
        avgLabel = QLabel('Среднее значение:', self)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(filenameLabel)
        layout.addWidget(self.filenameEdit)
        layout.addWidget(self.button)
        layout.addWidget(maxLabel)
        layout.addWidget(self.maxEdit)
        layout.addWidget(minLabel)
        layout.addWidget(self.minEdit)
        layout.addWidget(avgLabel)
        layout.addWidget(self.avgEdit)

        # Container widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

        # Connect button
        self.button.clicked.connect(self.calculate_statistics)

    def calculate_statistics(self):
        filename = self.filenameEdit.text()

        try:
            with open(filename, 'r') as file:
                content = file.read()

            # Extract integers
            numbers = []
            for part in content.split():
                if part.lstrip('-').isdigit():
                    numbers.append(int(part))

            if not numbers:
                raise ValueError('empty')

            max_val = max(numbers)
            min_val = min(numbers)
            avg_val = sum(numbers) / len(numbers)

            # Update output fields
            self.maxEdit.setText(str(max_val))
            self.minEdit.setText(str(min_val))
            self.avgEdit.setText(f"{avg_val:.2f}")

            # Save to out.txt
            with open('out.txt', 'w') as outfile:
                outfile.write(f"Максимальное значение = {max_val}\n")
                outfile.write(f"Минимальное значение = {min_val}\n")
                outfile.write(f"Среднее значение = {avg_val:.2f}\n")

            self.statusbar.showMessage('Рассчеты успешно выполнены', 5000)

        except FileNotFoundError:
            self.statusbar.showMessage('Указанный файл не существует', 5000)
            self.clear_outputs()

        except ValueError as e:
            if str(e) == 'empty':
                self.statusbar.showMessage('Указанный файл пуст', 5000)
            else:
                self.statusbar.showMessage('Файл содержит некорректные данные', 5000)
            self.clear_outputs()

    def clear_outputs(self):
        self.maxEdit.clear()
        self.minEdit.clear()
        self.avgEdit.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileStat()
    window.show()
    sys.exit(app.exec())
