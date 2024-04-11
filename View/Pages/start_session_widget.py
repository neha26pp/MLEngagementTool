import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
import os

from View.Pages.page import Page

video_directory = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(video_directory)


class StartSession(Page):
    def __init__(self, camera):
        super().__init__(heading_text="Start Session")
        self.camera = camera

        # create label to display camera
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        #  display a recording message
        self.message_label = QLabel("Please adjust the camera to make sure you are in the frame")
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setFixedHeight(80)

        # set layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.image_label)
        self.main_layout.addWidget(self.message_label)
        self.main_layout.addStretch(1)

    def open_camera(self):
        # create timer to update camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(50)

    def update_camera(self):
        ret, frame = self.camera.read()

        if ret:
            # flip the frame horizontally
            frame = cv2.flip(frame, 1)

            # convert cv2 image to Qt image
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = image.shape
            bytes_per_line = ch * w
            q_image = QImage(image.data, w, h, bytes_per_line, QImage.Format_RGB888)

            # display image on label
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            self.image_label.adjustSize()

    def stop_camera(self):
        # Stop the timer
        self.timer.stop()

        # Release the camera
        if self.camera.isOpened():
            self.camera.release()

        # Clear the image label
        self.image_label.clear()
