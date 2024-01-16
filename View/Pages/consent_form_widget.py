from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget


class ConsentFormWidget(QWidget):
    def __init__(self, consent_form, parent=None):
        super().__init__(parent)
        self.screen_layout = QVBoxLayout()
        self.consent_form = consent_form
        self.initUI()
    
    def initUI(self):
        # Create a label for "Consent Form" heading
        consent_form_heading = HeaderWidget("Consent Form")
        self.screen_layout.addWidget(consent_form_heading)
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://pennstate.qualtrics.com/jfe/form/SV_3yqNWDKN5PxuPoW"))

        # Create a checkbox for user agreement
        self.agree_checkbox = QCheckBox("I agree to the terms and conditions")

        # Set up screen layout
        self.screen_layout.addWidget(self.webview)
        self.screen_layout.addWidget(self.agree_checkbox)

        # Add reading material widget to screen layout
        self.setLayout(self.screen_layout)

    def connect_signals(self, update_next_button_func):
        self.agree_checkbox.stateChanged.connect(update_next_button_func)

    def get_checked(self):
        return self.agree_checkbox.checkState()

    def set_checked(self, is_checked):
        self.agree_checkbox.setChecked(is_checked)
