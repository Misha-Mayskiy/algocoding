import io
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QMainWindow, QApplication

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>827</width>
    <height>811</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QGridLayout" name="gridLayout">
    <item row="4" column="0" colspan="3">
     <widget class="QListWidget" name="listWidget"/>
    </item>
    <item row="3" column="0" colspan="3">
     <widget class="QPushButton" name="takeButton">
      <property name="text">
       <string>Взять</string>
      </property>
     </widget>
    </item>
    <item row="2" column="0">
     <widget class="QLabel" name="label_2">
      <property name="text">
       <string>Сколь камней взять?</string>
      </property>
     </widget>
    </item>
    <item row="2" column="1" colspan="2">
     <widget class="QLineEdit" name="takeInput"/>
    </item>
    <item row="0" column="0">
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Задать количество камней</string>
      </property>
     </widget>
    </item>
    <item row="0" column="1">
     <widget class="QSpinBox" name="stones"/>
    </item>
    <item row="1" column="0" colspan="3">
     <widget class="QLCDNumber" name="remainLcd"/>
    </item>
    <item row="0" column="2">
     <widget class="QPushButton" name="startButton">
      <property name="text">
       <string>Задать</string>
      </property>
     </widget>
    </item>
    <item row="5" column="0" colspan="3">
     <widget class="QLabel" name="resultLabel">
      <property name="text">
       <string/>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>827</width>
     <height>36</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""


class Pseudonym(QMainWindow):
    def __init__(self):
        super().__init__()

        f = io.StringIO(template)
        uic.loadUi(f, self)

        self.startButton.clicked.connect(self.start)
        self.takeButton.clicked.connect(self.take)

    def start(self):
        self.kamney = int(self.stones.text())
        self.remainLcd.display(self.kamney)
        self.listWidget.clear()
        self.resultLabel.setText('')

    def take(self):
        self.take_chel = int(self.takeInput.text())
        if self.kamney - self.take_chel == 0:
            self.listWidget.addItem(f'Игрок взял - {self.take_chel}')
            self.remainLcd.display(self.kamney - self.take_chel)
            self.resultLabel.setText('Победа пользователя!')
        else:
            self.kamney -= self.take_chel
            b = self.kamney % 4
            if b == 0:
                b = 2
            if b == 1:
                self.take_komp = 1
            else:
                self.take_komp = b
            self.kamney -= self.take_komp
            self.remainLcd.display(self.kamney)
            self.listWidget.addItem(f'Игрок взял - {self.take_chel}')
            self.listWidget.addItem(f'Компьютер взял - {self.take_komp}')
            if self.kamney == 0:
                self.resultLabel.setText('Победа компьютера!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Pseudonym()
    ex.show()
    sys.exit(app.exec())
