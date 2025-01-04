import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QLabel, QPushButton, QHBoxLayout, QDoubleSpinBox
)
from pyqtgraph import PlotWidget, plot


class FunctionPlotter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("График функции")
        self.setGeometry(100, 100, 800, 600)

        # Главный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Создание графического виджета
        self.graphWidget = PlotWidget()
        self.graphWidget.setBackground("w")  # Белый фон
        self.graphWidget.setLabel("left", "Y")  # Лейбл оси Y
        self.graphWidget.setLabel("bottom", "X")  # Лейбл оси X
        self.graphWidget.showGrid(x=True, y=True)  # Сетка

        # Поля ввода
        self.functionInput = QLineEdit()
        self.functionInput.setPlaceholderText("Введите функцию, например: np.sin(x) + x**2")

        self.startInput = QDoubleSpinBox()
        self.startInput.setRange(-10000, 10000)
        self.startInput.setValue(-10)

        self.endInput = QDoubleSpinBox()
        self.endInput.setRange(-10000, 10000)
        self.endInput.setValue(10)

        self.plotButton = QPushButton("Построить график")
        self.plotButton.clicked.connect(self.plot_function)

        # Макет интерфейса
        inputLayout = QHBoxLayout()
        inputLayout.addWidget(QLabel("Функция:"))
        inputLayout.addWidget(self.functionInput)
        inputLayout.addWidget(QLabel("Диапазон (начало и конец):"))
        inputLayout.addWidget(self.startInput)
        inputLayout.addWidget(self.endInput)
        inputLayout.addWidget(self.plotButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.graphWidget)
        mainLayout.addLayout(inputLayout)

        self.central_widget.setLayout(mainLayout)

    def plot_function(self):
        """Функция для построения графика."""
        try:
            # Получение данных от пользователя
            func_text = self.functionInput.text()
            x_start = self.startInput.value()
            x_end = self.endInput.value()

            # Проверка диапазона
            if x_start >= x_end:
                self.show_error("Начало диапазона должно быть меньше конца!")
                return

            # Создание массива значений X
            x = np.linspace(x_start, x_end, 1000)

            # Вычисление Y на основе введённой функции
            y = eval(func_text, {"x": x, "np": np})

            # Очистка графика и построение нового
            self.graphWidget.clear()
            self.graphWidget.plot(x, y, pen="b", name="График функции")

        except Exception as e:
            self.show_error(f"Ошибка: {str(e)}")

    def show_error(self, message):
        """Показ сообщения об ошибке."""
        errorLabel = QLabel(message)
        errorLabel.setStyleSheet("color: red;")
        self.central_widget.layout().addWidget(errorLabel)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FunctionPlotter()
    window.show()
    sys.exit(app.exec())
