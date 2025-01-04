import sys
import csv
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem


class InteractiveReceipt(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Price Table")
        self.setGeometry(100, 100, 600, 400)

        self.tableWidget = QTableWidget()
        self.setCentralWidget(self.tableWidget)

        self.load_data('price.csv')

        self.tableWidget.cellChanged.connect(self.update_total)

    def load_data(self, file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            for row in reader:
                data.append(row)

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(["Название товара", "Цена", "Количество", "Total"])

        for row_index, row_data in enumerate(data):
            name_item = QTableWidgetItem(row_data[0])
            price_item = QTableWidgetItem(row_data[1])
            quantity_item = QTableWidgetItem("0")
            total = QTableWidgetItem("0")

            self.tableWidget.setItem(row_index, 0, name_item)
            self.tableWidget.setItem(row_index, 1, price_item)
            self.tableWidget.setItem(row_index, 2, quantity_item)
            self.tableWidget.setItem(row_index, 3, total)

    def update_total(self, row, column):
        if column == 2:  # Если изменено количество
            price_item = self.tableWidget.item(row, 1)
            quantity_item = self.tableWidget.item(row, 2)
            total_item = self.tableWidget.item(row, 3)

            price = int(price_item.text())
            quantity = int(quantity_item.text())
            total = price * quantity

            total_item.setText(str(total))


def main():
    app = QApplication(sys.argv)
    window = InteractiveReceipt()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
