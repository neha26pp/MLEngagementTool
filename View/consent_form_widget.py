from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from header_widget import HeaderWidget


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
        self.screen_layout.addWidget(self.webview)

        # # Add reading material widget to screen layout
        self.setLayout(self.screen_layout)
