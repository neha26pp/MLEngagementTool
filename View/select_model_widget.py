import sys
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from View.header_widget import HeaderWidget


class SelectModelWidget(QWidget):
    model_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # create header
        header = HeaderWidget("Analyze Data")

        # create title label
        title_label = QLabel("Select Model")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # Create radio buttons
        self.radio_svr_eye = QRadioButton("SVR Eye")
        self.radio_svr_emotion = QRadioButton("SVR Emotion")
        self.radio_svr_fusion = QRadioButton("SVR Fusion")

        # Connect toggled signals to a method using lambda
        self.radio_svr_eye.toggled.connect(lambda: self.model_selected.emit("eye"))
        self.radio_svr_emotion.toggled.connect(lambda: self.model_selected.emit("emotion"))
        self.radio_svr_fusion.toggled.connect(lambda: self.model_selected.emit("fusion"))

        # Set up layout
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.radio_svr_eye)
        button_layout.addWidget(self.radio_svr_emotion)
        button_layout.addWidget(self.radio_svr_fusion)
        button_group_layout = QHBoxLayout()
        button_group_layout.addStretch(1)
        button_group_layout.addLayout(button_layout)
        button_group_layout.addStretch(1)

        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addStretch(1)
        main_layout.addLayout(button_group_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     screen = SelectModelWidget()
#     screen.setGeometry(100, 100, 1000, 800)
#     screen.show()
#     sys.exit(app.exec_())
