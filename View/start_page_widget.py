import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import *
from header_widget import HeaderWidget


class StartPage(QWidget):
    collect_data_clicked = pyqtSignal()
    analyze_data_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        # create header
        header = HeaderWidget("")

        # create title label
        title_label = QLabel("Student Engagement Tool")
        title_label.setObjectName("startPageTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # create buttons
        collect_data_button = QPushButton("Collect Data", self)
        collect_data_button.setObjectName("startPageButton")
        collect_data_button.setFixedSize(450, 375)

        collect_data_button.clicked.connect(self.collect_data_clicked.emit)

        analyze_data_button = QPushButton("Analyze Data", self)
        analyze_data_button.setObjectName("startPageButton")
        analyze_data_button.setFixedSize(450, 375)
        analyze_data_button.clicked.connect(self.analyze_data_clicked.emit)

        # set layout
        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        
        main_layout.addWidget(header)

        main_layout.addWidget(title_label)
        main_layout.addSpacing(80)
        button_layout.addWidget(collect_data_button)
        button_layout.addWidget(analyze_data_button)

        button_layout_widget = QWidget()
        button_layout_widget.setLayout(button_layout)

        main_layout.addWidget(button_layout_widget)
        main_layout.addStretch(1)

        self.setLayout(main_layout)


# if __name__ == "__main__":

#     app = QApplication(sys.argv)
#     self.setWindowTitle("Start Page")
#     self.setGeometry(100, 100, 400, 200)
#     start_page = StartPage()
#     start_page.show()
#     sys.exit(app.exec_())