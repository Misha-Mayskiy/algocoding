import sys
import pandas as pd
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QWidget
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt


class TitanicSearch(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Поиск на Титанике")

        # Загрузка данных из CSV
        self.data = pd.read_csv("titanic.csv")

        # Главный виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Строка поиска
        self.searchEdit = QLineEdit()
        self.searchEdit.setPlaceholderText("Подстрока для поиска:")
        self.searchEdit.textChanged.connect(self.update_table)

        # Таблица
        self.resultTable = QTableWidget()
        self.resultTable.setColumnCount(len(self.data.columns))
        self.resultTable.setHorizontalHeaderLabels(self.data.columns)
        self.resultTable.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.resultTable.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # Макет
        layout = QVBoxLayout()
        layout.addWidget(self.searchEdit)
        layout.addWidget(self.resultTable)
        self.central_widget.setLayout(layout)

        # Обновление таблицы
        self.update_table()

    def update_table(self):
        search_text = self.searchEdit.text().strip().lower()

        # Фильтрация данных
        if len(search_text) < 3:
            filtered_data = self.data
        else:
            filtered_data = self.data[self.data["Name"].str.strip().str.lower().str.contains(search_text, na=False)]

        # Полное обновление таблицы
        self.resultTable.clear()  # Полностью очищаем таблицу
        self.resultTable.setRowCount(len(filtered_data))  # Устанавливаем количество строк
        self.resultTable.setColumnCount(len(self.data.columns))  # Устанавливаем количество столбцов
        self.resultTable.setHorizontalHeaderLabels(self.data.columns)  # Устанавливаем заголовки колонок

        for row_idx, row in filtered_data.iterrows():
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                self.resultTable.setItem(row_idx, col_idx, item)

                # Раскраска строк
                if row["Survived"] == 1:
                    item.setBackground(QColor("#00FF00"))  # Зеленый для выживших
                else:
                    item.setBackground(QColor("#FF0000"))  # Красный для погибших

        self.resultTable.resizeColumnsToContents()  # Подгоняем размеры колонок


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = TitanicSearch()
    window.show()

    sys.exit(app.exec())
