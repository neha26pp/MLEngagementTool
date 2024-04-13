from PyQt5.QtCore import QSize
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import *

HEADER_H = 120  # header bar widget height


class HeaderWidget(QWidget):
    def __init__(self, heading_text=None):
        super().__init__()
        self.heading_label = QLabel(heading_text)  # Make it an instance variable
        self.heading_label.setStyleSheet("color: white;")
        self.initUI(heading_text)

    def initUI(self, heading_text):
        # Create logo svg widget
        svg_widget = QSvgWidget("../static/psu-mark.svg")
        svg_widget.setFixedSize(QSize(80, 90))

        # Create a horizontal header layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(self.heading_label)  # Use the instance variable
        header_layout.addWidget(svg_widget)
        header_layout.addSpacing(30)

        # Create a widget to contain header layout
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setObjectName("headerWidget")
        self.setFixedHeight(HEADER_H)

        # Set the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(header_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

    def update_text(self, new_text):
        self.heading_label.setText(new_text)  # Update the text of the QLabel
