from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from View.Components.header_widget import HeaderWidget


class Page(QWidget):
    def __init__(self, heading_text):
        super().__init__()
        self.header = HeaderWidget(heading_text)
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)





