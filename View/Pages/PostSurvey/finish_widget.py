from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget
from View.Pages.page import Page


class FinishWidget(Page):

    def __init__(self):
        super().__init__(heading_text="do not show")
        self.screen_HLayout = QHBoxLayout()
        self.go_to_dashboard_button = QPushButton("Go back to Dashboard")
        self.store_data_button = QPushButton("Store Data")

        self.initUI()

    def initUI(self):
        try:
            # Set finish heading
            self.completed_label = QLabel("Thank You!\nYour responses have been recorded.")
            self.completed_label.setAlignment(Qt.AlignCenter)
            self.completed_label.setFixedHeight(400)
            self.completed_label.setObjectName("completeMessage")

            # Set go to dashboard button
            self.go_to_dashboard_button.setFixedSize(500, 200)
            self.go_to_dashboard_button.setObjectName("goToDashboardButton")

            # Set store data button
            self.store_data_button.setFixedSize(500, 200)
            self.store_data_button.setObjectName("storeDataButton")

            # Create a horizontal layout for buttons
            buttons_layout = QHBoxLayout()
            buttons_layout.addWidget(self.go_to_dashboard_button)
            buttons_layout.addWidget(self.store_data_button)

            # Set layout
            self.main_layout.setAlignment(Qt.AlignCenter)
            self.main_layout.addStretch(1)
            self.main_layout.addWidget(self.completed_label, alignment=Qt.AlignCenter)
            self.main_layout.addLayout(buttons_layout)  # Add the buttons layout here
            self.main_layout.addStretch(1)

        except Exception as e:
            print("An error occurred in FinishWidget widget:", str(e))
