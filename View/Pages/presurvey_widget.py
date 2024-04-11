from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Pages.page import Page


class PreSurveyWidget(Page):
    def __init__(self, pre_survey):
        super().__init__(heading_text="Pre Survey")
        self.pre_survey = pre_survey
        self.main_layout.addWidget(self.header)

        # need to change this link
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://pennstate.qualtrics.com/jfe/form/SV_bsjWFpVIK6QKdYa"))
        self.main_layout.addWidget(self.webview)


    def show_recording_message(self, message):
        # Display a message saying "Recording will begin on next page"
        self.recording_message = QLabel(message)
        self.recording_message.setObjectName("recording_message")
        self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        self.main_layout.addWidget(self.recording_message)

        # Start the flash timer to make the message flash
        self.flash_timer.timeout.connect(self.toggle_flash)
        self.flash_timer.start(500)  # Adjust the flash interval (in milliseconds) based on your preference

    def toggle_flash(self):
        # Toggle the flash state and update the message visibility accordingly
        self.flash_state = not self.flash_state
        self.recording_message.setVisible(self.flash_state)

        # Check if the maximum number of flashes is reached
        if self.flash_state and self.flash_count >= self.max_flash_count:
            self.flash_timer.stop()
            self.hide_recording_message()

        # Increment the flash count if the message is visible
        if self.flash_state:
            self.flash_count += 1

    def hide_recording_message(self):
        # Remove the recording message widget
        if self.recording_message:
            self.main_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None