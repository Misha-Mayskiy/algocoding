from PyQt6.QtWidgets import *


class SimplePlanner(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Simple Planner')

        layout = QVBoxLayout(self)

        self.lineEdit = QLineEdit(self)  # Поле для ввода названия события
        layout.addWidget(self.lineEdit)

        self.calendarWidget = QCalendarWidget(self)
        layout.addWidget(self.calendarWidget)

        self.timeEdit = QTimeEdit(self)
        layout.addWidget(self.timeEdit)

        self.addEventBtn = QPushButton('Добавить событие', self)
        layout.addWidget(self.addEventBtn)

        self.eventList = QListWidget(self)
        layout.addWidget(self.eventList)

        self.addEventBtn.clicked.connect(self.add_event)

        self.events = []

    def add_event(self):
        date = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')
        time = self.timeEdit.time().toString('HH:mm:ss')
        task = self.lineEdit.text()  # Получаем текст задачи
        event_text = f"{date} {time} - {task}"

        # Добавляем событие в список
        self.events.append(event_text)

        # Сортируем события по дате и времени
        self.events.sort()

        # Очищаем список и добавляем отсортированные события
        self.eventList.clear()
        self.eventList.addItems(self.events)


if __name__ == "__main__":
    app = QApplication([])
    window = SimplePlanner()
    window.show()
    app.exec()
