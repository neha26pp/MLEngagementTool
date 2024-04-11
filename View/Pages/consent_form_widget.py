from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget
from View.Pages.page import Page


class ConsentFormWidget(Page):
    def __init__(self, consent_form, heading_text="Consent Form"):
        super().__init__(heading_text)
        self.consent_form = consent_form

        # Create a label for "Consent Form" heading
        self.main_layout.addWidget(self.header)
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://pennstate.qualtrics.com/jfe/form/SV_3yqNWDKN5PxuPoW"))

        # Create a checkbox for user agreement
        self.agree_checkbox = QCheckBox("I agree to the terms and conditions")

        # Set up screen layout
        self.main_layout.addWidget(self.webview)
        self.main_layout.addWidget(self.agree_checkbox)

    # consent form widget
    def connect_signals(self, update_next_button_func):
        self.agree_checkbox.stateChanged.connect(update_next_button_func)

    def get_checked(self):
        return self.agree_checkbox.checkState()

    def set_checked(self, is_checked):
        self.agree_checkbox.setChecked(is_checked)
