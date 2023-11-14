import os
import sys
import yaml
from pathlib import Path
import random

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QTimer

class IndividualInterestSurveyWidget(QWidget):
    def __init__(self, individual_interest_survey, next_button, parent=None):
        super().__init__(parent)
        self.individual_interest_survey = individual_interest_survey
        self.screen_layout = QVBoxLayout()
        self.emotional_analysis = emotional_analysis
       
        
        self.next_button = next_button
       
        self.recording_message = None
        self.flash_timer = QTimer(self)
        self.flash_state = False
        self.flash_count = 0
        self.max_flash_count = 2  # Set the maximum number of flashes

        self.initUI()


    def initUI(self):
        # Create a label for "Individual Interest survey" heading
        individual_interest_survey_heading = QLabel("Individual Interest Survey")
        individual_interest_survey_heading.setObjectName("heading1")
        individual_interest_survey_heading.setFixedHeight(75)
        self.screen_layout.addWidget(individual_interest_survey_heading)

        # need to change this link
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://pennstate.qualtrics.com/jfe/form/SV_ePemJZMDNvvk9VQ"))
        self.screen_layout.addWidget(self.webview)

        self.setLayout(self.screen_layout)

    def show_recording_message(self, message):
        # Display a message saying "Recording will begin on next page"
        self.recording_message = QLabel(message)
        self.recording_message.setObjectName("recording_message")
        self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        self.screen_layout.addWidget(self.recording_message)

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
            self.screen_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None