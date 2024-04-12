from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget
from View.Pages.page import Page


class FinishWidget(Page):

    def __init__(self):
        super().__init__(heading_text="do not show")
        self.screen_HLayout = QHBoxLayout()
        self.go_to_dashboard_button = QPushButton("Go back to Dashboard")

        self.initUI()

    def initUI(self):
        try:
            # Set finish heading
            self.main_layout.setAlignment(Qt.AlignCenter)
            self.completed_label = QLabel("Thank You!\n Your responses have been recorded.")
            self.completed_label.setAlignment(Qt.AlignCenter)
            self.completed_label.setFixedHeight(400)
            self.completed_label.setObjectName("completeMessage")

            # Set go to dashboard button
            self.go_to_dashboard_button.setFixedSize(500, 200)
            self.go_to_dashboard_button.setObjectName("goToDashboardButton")

            # Set layout
            self.main_layout.setAlignment(Qt.AlignCenter)
            self.main_layout.addStretch(1)
            self.screen_HLayout.addWidget(self.completed_label, 1)
            self.main_layout.addLayout(self.screen_HLayout)
            self.main_layout.addWidget(self.go_to_dashboard_button, alignment=Qt.AlignCenter)
            self.main_layout.addStretch(1)

        except Exception as e:
            print("An error occurred in FinishWidget widget:", str(e))
