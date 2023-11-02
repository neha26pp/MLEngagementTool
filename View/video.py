# Play the video for the student
from PyQt5 import QtWidgets, QtCore, QtGui
import sys, time
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import * 

class Video(QWidget):

    '''Display the youtube video to student'''
    def __init__(self, parent=None):
        super(Video, self).__init__(parent)
        self.vlayout = QVBoxLayout()
        self.webview = QWebEngineView()
        self.webview.setUrl(QUrl("https://youtu.be/6AviDjR9mmo?si=hXVZi71tqf2Vm5Vm"))
        self.vlayout.addWidget(self.webview)
        # self.show()