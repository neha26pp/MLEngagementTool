from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget


class FinishWidget(QWidget):
    go_to_dashboard_button_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.screen_layout = QVBoxLayout()
        self.screen_HLayout = QHBoxLayout()
        self.go_to_dashboard_button = QPushButton("Go back to Dashboard")

        self.initUI()

    def initUI(self):
        try:
            # Set finish heading
            self.finish_heading = HeaderWidget("Finish")

            self.screen_layout = QVBoxLayout()
            self.screen_layout.setAlignment(Qt.AlignCenter)

            self.completed_label = QLabel("Thank You!\n Your responses have been recorded.")
            self.completed_label.setAlignment(Qt.AlignCenter)
            self.completed_label.setFixedHeight(400)
            self.completed_label.setObjectName("completeMessage")

            # Set go to dashboard button
            self.go_to_dashboard_button_signal.emit()
            self.go_to_dashboard_button.setFixedSize(500, 200)
            self.go_to_dashboard_button.setObjectName("goToDashboardButton")

            # Set layout
            self.screen_layout.setAlignment(Qt.AlignCenter)
            self.screen_layout.addWidget(self.finish_heading)
            self.screen_layout.addStretch(1)
            self.screen_HLayout.addWidget(self.completed_label, 1)
            self.screen_layout.addLayout(self.screen_HLayout)
            self.screen_layout.addWidget(self.go_to_dashboard_button, alignment=Qt.AlignCenter)
            self.screen_layout.addStretch(1)

            self.setLayout(self.screen_layout)
        except Exception as e:
            print("An error occurred in FinishWidget widget:", str(e))
