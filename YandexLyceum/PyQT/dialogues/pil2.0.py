import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog, QLabel,
                             QPushButton, QGridLayout, QWidget, QButtonGroup, QHBoxLayout, QVBoxLayout)
from PyQt6.QtGui import QImage, QPixmap, QTransform
from PyQt6.QtCore import Qt


class MyPillow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.curr_image = QImage()
        self.original_image = QImage()

        self.rotation_angle = 0
        self.current_channel = -1

        self.initUI()

    def initUI(self):
        self.setWindowTitle('PIL 2.0')

        # Create widgets
        self.imageLabel = QLabel(self)
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rotateLeftButton = QPushButton('Против часовой стрелки', self)
        self.rotateLeftButton.clicked.connect(self.rotate_counter_clockwise)

        self.rotateRightButton = QPushButton('По часовой стрелке', self)
        self.rotateRightButton.clicked.connect(self.rotate_clockwise)

        self.redButton = QPushButton('R', self)
        self.redButton.clicked.connect(self.show_red_channel)

        self.greenButton = QPushButton('G', self)
        self.greenButton.clicked.connect(self.show_green_channel)

        self.blueButton = QPushButton('B', self)
        self.blueButton.clicked.connect(self.show_blue_channel)

        self.allButton = QPushButton('ALL', self)
        self.allButton.clicked.connect(self.show_all_channels)

        # Create button groups
        self.channelButtons = QButtonGroup(self)
        self.channelButtons.addButton(self.redButton)
        self.channelButtons.addButton(self.greenButton)
        self.channelButtons.addButton(self.blueButton)
        self.channelButtons.addButton(self.allButton)

        self.rotateButtons = QButtonGroup(self)
        self.rotateButtons.addButton(self.rotateLeftButton)
        self.rotateButtons.addButton(self.rotateRightButton)

        # Layout
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(self.redButton)
        buttonLayout.addWidget(self.greenButton)
        buttonLayout.addWidget(self.blueButton)
        buttonLayout.addWidget(self.allButton)
        buttonLayout.addStretch()

        rotateLayout = QHBoxLayout()
        rotateLayout.addWidget(self.rotateLeftButton)
        rotateLayout.addWidget(self.rotateRightButton)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.imageLabel, 0, 0, 1, 2)
        mainLayout.addLayout(buttonLayout, 1, 0)
        mainLayout.addLayout(rotateLayout, 2, 0, 1, 2)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        file_name = QFileDialog.getOpenFileName(self, "Выберите изображение", "",
                                                "Images (*.png *.xpm *.jpg *.bmp);;All Files (*)")[0]
        if file_name:
            self.load_image(file_name)

    def load_image(self, file_name):
        self.original_image.load(file_name)
        self.curr_image = self.original_image.copy()
        self.update_image()

    def update_image(self):
        pixmap = QPixmap.fromImage(self.curr_image)
        self.imageLabel.setPixmap(pixmap.scaled(self.imageLabel.size(), Qt.AspectRatioMode.KeepAspectRatio))

    def get_current_transform(self):
        transform = QTransform()
        angle = self.rotation_angle % 360  # Ограничиваем значение угла
        transform.rotate(angle)
        return transform

    def rotate_counter_clockwise(self):
        self.rotation_angle -= 90
        self.apply_channel_filter(self.current_channel)

    def rotate_clockwise(self):
        self.rotation_angle += 90
        self.apply_channel_filter(self.current_channel)

    def show_red_channel(self):
        self.apply_channel_filter(0)

    def show_green_channel(self):
        self.apply_channel_filter(1)

    def show_blue_channel(self):
        self.apply_channel_filter(2)

    def show_all_channels(self):
        self.apply_channel_filter(-1)

    def apply_channel_filter(self, channel):
        self.current_channel = channel
        rotated_image = self.original_image.transformed(self.get_current_transform())
        rotated_image = rotated_image.convertToFormat(QImage.Format.Format_RGB32)
        for y in range(rotated_image.height()):
            for x in range(rotated_image.width()):
                pixel = rotated_image.pixel(x, y)
                r = (pixel >> 16) & 0xff
                g = (pixel >> 8) & 0xff
                b = pixel & 0xff
                if channel == 0:  # Красный канал
                    rotated_image.setPixel(x, y, (r << 16) | 0 | 0)
                elif channel == 1:  # Зелёный канал
                    rotated_image.setPixel(x, y, (0 << 16) | (g << 8) | 0)
                elif channel == 2:  # Синий канал
                    rotated_image.setPixel(x, y, (0 << 16) | 0 | b)
                elif channel == -1:  # Все каналы
                    rotated_image.setPixel(x, y, (r << 16) | (g << 8) | b)
        self.curr_image = rotated_image
        self.update_image()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPillow()
    ex.show()
    sys.exit(app.exec())
