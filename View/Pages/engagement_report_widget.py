import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from View.Components.header_widget import HeaderWidget
from View.Components.bar_chart_widget import BarChartWidget

class EngagementReportWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.student_data = None
        self.select_model = None

        # create header
        header = HeaderWidget("Analyze Data")

        # create title label
        title_label = QLabel("Engagement Report")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # Create radio buttons
        self.radio_svr_eye = QRadioButton("SVR Eye")
        self.radio_svr_emotion = QRadioButton("SVR Emotion")
        self.radio_svr_fusion = QRadioButton("SVR Fusion")

        # Connect toggled signals to a method using lambda
        self.radio_svr_eye.toggled.connect(lambda: self.update_student_data(self.student_data, "SVR Eye"))
        self.radio_svr_emotion.toggled.connect(lambda: self.update_student_data(self.student_data, "SVR Emotion"))
        self.radio_svr_fusion.toggled.connect(lambda: self.update_student_data(self.student_data, "SVR Fusion"))

        # Set up layout
        button_HLayout = QHBoxLayout()
        button_HLayout.addWidget(self.radio_svr_eye)
        button_HLayout.addWidget(self.radio_svr_emotion)
        button_HLayout.addWidget(self.radio_svr_fusion)

        # Set up report layout
        self.report_HLayout = QHBoxLayout()
        no_data_label = QLabel("No data available")
        self.report_HLayout.addWidget(no_data_label)
        self.report_HLayout.addStretch(1)

        self.report_widget = QWidget()
        self.report_widget.setLayout(self.report_HLayout)

        # Set up main layout
        self.screen_layout = QVBoxLayout()
        self.screen_layout.setAlignment(Qt.AlignCenter)
        self.screen_layout.addWidget(header)
        self.screen_layout.addLayout(button_HLayout)
        self.screen_layout.addWidget(title_label)
        self.screen_layout.addWidget(self.report_widget)

        self.setLayout(self.screen_layout)

    def update_student_data(self, student_data=None, select_model="SVR Eye"):
        try:
            self.student_data = student_data
            self.select_model = select_model

            # Clear existing report widget
            self.screen_layout.removeWidget(self.report_widget)
            self.report_widget.deleteLater()

            # Create new report widget
            self.report_HLayout = QHBoxLayout()
            self.report_widget = QWidget()

            if self.student_data is not None:
                # student info
                name = student_data.get("name")
                stimulus1 = student_data.get("stimulus1")
                stimulus2 = student_data.get("stimulus2")
                # score = student_data.get(select_model)

                name_label = QLabel("Name: " + name)
                stimulus1_label = QLabel("stimulus 1: " + stimulus1)
                stimulus2_label = QLabel("stimulus 2: " + stimulus2)
                # score_label = QLabel(select_model + " Score: " + str(score) + "%")
                # score_label.setObjectName("score")
                # score_label.setAlignment(Qt.AlignCenter)

                # Curve chart
                # image_label = QLabel()

                # Load the image from the file path
                # pixmap = QPixmap("../quiz_data/score_curve_simple.jpg")

                # if pixmap.isNull():
                #     image_label.setText("no image available")
                # else:
                #     # Set the pixmap to the QLabel
                #     image_label.setPixmap(pixmap)
                #     image_label.setAlignment(Qt.AlignCenter)

                # Bar chart
                categories = ['SVR Eye', 'SVR Emotion', 'SVR Fusion']
                scores = [student_data.get(c) for c in categories]
                bar_chart_widget = BarChartWidget(categories, scores)

                # Set stimulus data to QLabel
                stimulus_layout = QVBoxLayout()
                stimulus_layout.addWidget(name_label)
                stimulus_layout.addWidget(stimulus1_label)
                stimulus_layout.addWidget(stimulus2_label)
                stimulus_layout.addStretch(1)

                score_layout = QVBoxLayout()
                # score_layout.addWidget(score_label)
                score_layout.addWidget(bar_chart_widget)
                score_layout.addStretch(1)

                self.report_HLayout.addStretch(1)
                self.report_HLayout.addLayout(stimulus_layout)
                self.report_HLayout.addStretch(1)
                self.report_HLayout.addLayout(score_layout)

            else:
                no_data_label = QLabel("No data available")
                self.report_HLayout.addWidget(no_data_label)

            self.report_widget.setLayout(self.report_HLayout)
            self.report_HLayout.addStretch(1)
            self.screen_layout.addWidget(self.report_widget)
        except Exception as e:
            print("An error occurred in update_student_data:", str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = EngagementReportWidget()
    screen.setGeometry(100, 100, 1600, 1200)
    screen.show()
    sys.exit(app.exec_())
