from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from View.Components.header_widget import HeaderWidget


class Page(QWidget):
    def __init__(self, heading_text):
        super().__init__()
        self.heading_text = heading_text
        
        self.main_layout = QVBoxLayout()
        if(self.heading_text != "do not show"):
            self.header = HeaderWidget(self.heading_text)
            self.main_layout.addWidget(self.header)
        self.setLayout(self.main_layout)
    
    def update_header(self, new_heading_text):
        self.heading_text = new_heading_text
        self.header.update_text(new_heading_text)  # Assuming HeaderWidget has an update_text method to set new text






