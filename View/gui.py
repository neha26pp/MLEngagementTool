from PyQt5 import QtWidgets, QtCore, QtGui
import sys, time
from PyQt5.QtCore import *
from PyQt5 import QtWebEngineWidgets
from PyQt5 import QtWebEngineCore
from PyQt5.QtWebEngineWidgets import *

from PyQt5.QtWidgets import * 

class Gui(QWidget):
    '''Welcome screen with 2 options - Collect Data OR Analyze Data'''

    def __init__(self, parent):
        super(Gui, self).__init__()
        self.parent = parent
        self.vlayout = QHBoxLayout()
        self.collectDataBtn = QPushButton("Collect Data", self)
        self.collectDataBtn.clicked.connect(self.parent.collectDataBtn_pressed)
        self.analyzeDataBtn = QPushButton("Analyze Data", self)
        self.analyzeDataBtn.clicked.connect(self.parent.analyzeDataBtn_pressed)

        self.vlayout.addWidget(self.collectDataBtn)
        self.vlayout.addWidget(self.analyzeDataBtn)

        self.setLayout(self.vlayout)
        self.show()
