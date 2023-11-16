from PyQt5.QtCore import Qt, QSize
from PyQt5.QtSvg import QSvgWidget
from PyQt5.QtWidgets import *
from constant import *


class HeaderWidget(QWidget):
    def __init__(self, heading_text=None):
        super().__init__()
        self.initUI(heading_text)

    def initUI(self, heading_text):
        # create heading label
        heading_label = QLabel(heading_text)
        heading_label.setObjectName("heading1")

        # create logo svg widget
        svg_widget = QSvgWidget("../static/psu-mark.svg")
        svg_widget.setFixedSize(QSize(80, 90))

        # create a horizontal header layout
        header_layout = QHBoxLayout()
        header_layout.addWidget(heading_label)
        header_layout.addWidget(svg_widget)
        header_layout.addSpacing(30)

        # create a widget to contain header layout
        header_widget = QWidget()
        header_widget.setLayout(header_layout)
        header_widget.setObjectName("headerWidget")
        self.setFixedHeight(HEADER_H)

        # set the layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(header_widget)
        self.setLayout(main_layout)
