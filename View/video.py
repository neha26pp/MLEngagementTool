# Play the video for the student
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import * 

class Video(QWidget):

    """Display the YouTube video to student"""
    def __init__(self, parent=None):
        super(Video, self).__init__(parent)
        self.vlayout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://youtu.be/6AviDjR9mmo?si=hXVZi71tqf2Vm5Vm"))
        self.vlayout.addWidget(self.webview)
