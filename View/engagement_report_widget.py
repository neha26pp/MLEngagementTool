import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from View.header_widget import HeaderWidget


class EngagementReportWidget(QWidget):

    def __init__(self, student_data=None, model=None):
        super().__init__()
        self.student_data = student_data

    def update_student_data(self, student_data):
        self.student_data = student_data

        # create header
        header = HeaderWidget("Analyze Data")

        # create title label
        title_label = QLabel("Engagement Report")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # Set up layout
        report_layout = QHBoxLayout()
        report_layout.addStretch(1)
        if self.student_data is not None:
            # info
            name = student_data.get("name")
            stimulus1 = student_data.get("stimulus1")
            stimulus2 = student_data.get("stimulus2")
            score = student_data.get("score")
            name_label = QLabel("Name: " + name)
            name_label.setObjectName("score")
            stimulus1_label = QLabel("stimulus 1: " + stimulus1)
            stimulus2_label = QLabel("stimulus 2: " + stimulus2)
            score_label = QLabel("Total Score: " + str(score) + "%")
            score_label.setObjectName("score")
            score_label.setAlignment(Qt.AlignCenter)

            # curve chart
            image_label = QLabel()

            # Load the image from the file path
            pixmap = QPixmap("../quiz_data/score_curve_simple.jpg")

            # Set the pixmap to the QLabel
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            stimulus_layout = QVBoxLayout()
            stimulus_layout.addWidget(name_label)
            stimulus_layout.addWidget(stimulus1_label)
            stimulus_layout.addWidget(stimulus2_label)
            stimulus_layout.addStretch(1)

            score_layout = QVBoxLayout()
            score_layout.addWidget(score_label)
            score_layout.addWidget(image_label)

            report_layout.addLayout(stimulus_layout)
            report_layout.addStretch(1)
            report_layout.addLayout(score_layout)
        else:
            no_data_label = QLabel("No data available")
            report_layout.addWidget(no_data_label)
        report_layout.addStretch(1)

        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addLayout(report_layout)
        print("update_student_data:", self.student_data)

        self.setLayout(main_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = EngagementReportWidget()
    screen.setGeometry(100, 100, 1000, 800)
    screen.show()
    sys.exit(app.exec_())
