import sys

from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QCheckBox


class WidgetsHideNSeek(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 150)
        self.setWindowTitle('Прятки для виджетов')

        self.checkbox1 = QCheckBox('edit1', self)
        self.checkbox1.setChecked(True)
        self.checkbox1.move(10, 13)
        self.checkbox1.clicked.connect(self.toggle_edit)

        self.edit1 = QLineEdit('Поле edit1', self)
        self.edit1.move(70, 10)

        self.checkbox2 = QCheckBox('edit2', self)
        self.checkbox2.setChecked(True)
        self.checkbox2.move(10, 43)
        self.checkbox2.clicked.connect(self.toggle_edit)

        self.edit2 = QLineEdit('Поле edit2', self)
        self.edit2.move(70, 40)

        self.checkbox3 = QCheckBox('edit3', self)
        self.checkbox3.setChecked(True)
        self.checkbox3.move(10, 73)
        self.checkbox3.clicked.connect(self.toggle_edit)

        self.edit3 = QLineEdit('Поле edit3', self)
        self.edit3.move(70, 70)

        self.checkbox4 = QCheckBox('edit4', self)
        self.checkbox4.setChecked(True)
        self.checkbox4.move(10, 103)
        self.checkbox4.clicked.connect(self.toggle_edit)

        self.edit4 = QLineEdit('Поле edit4', self)
        self.edit4.move(70, 100)

        self.controls = {
            'edit1': self.edit1,
            'edit2': self.edit2,
            'edit3': self.edit3,
            'edit4': self.edit4,
        }

    def toggle_edit(self):
        sender: QCheckBox = self.sender()
        control = self.controls[sender.text()]
        if sender.isChecked():
            control.show()
        else:
            control.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = WidgetsHideNSeek()
    form.show()
    sys.exit(app.exec())
