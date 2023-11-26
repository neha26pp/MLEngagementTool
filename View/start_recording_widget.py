import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *

from View.header_widget import HeaderWidget

class StartRecording(QWidget):
    def __init__(self):
        super().__init__()
        header = HeaderWidget("Starting Recording")

        # create label to display camera
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.addWidget(self.image_label)

        # open camera
        self.camera = cv2.VideoCapture(0)

        # create timer to update camera
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_camera)
        self.timer.start(50)

        # set layout for the main widget
        self.setLayout(main_layout)

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
        # Release the camera when closing the window
        self.camera.release()


# if __name__ == "__main__":

#     app = QApplication(sys.argv)
#     self.setWindowTitle("Start Recording")
#     self.setGeometry(100, 100, 400, 200)
#     start_page = StartPage()
#     start_page.show()
#     sys.exit(app.exec_())
