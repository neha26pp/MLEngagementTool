import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from View.Components.bar_chart_widget import BarChartWidget
from View.Pages.page import Page


class EngagementReportWidget(Page):
    def __init__(self):
        super().__init__(heading_text="Analyze Data")
        self.student_data = None

        # create title label
        title_label = QLabel("Engagement Report")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # Set up report layout
        self.report_HLayout = QHBoxLayout()
        no_data_label = QLabel("No data available")
        self.report_HLayout.addWidget(no_data_label)
        self.report_HLayout.addStretch(1)

        self.report_widget = QWidget()
        self.report_widget.setLayout(self.report_HLayout)

        # Set up main layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(self.report_widget)

    def update_student_data(self, student_data):
        try:
            self.student_data = student_data
            # Clear existing report widget
            self.main_layout.removeWidget(self.report_widget)
            self.report_widget.deleteLater()

            # Create new report widget
            self.report_HLayout = QHBoxLayout()
            self.report_widget = QWidget()
            print(self.student_data)

            if self.student_data is not None:
                # student info
                name = student_data.get("name")
                stimulus1 = student_data.get("stimulus1")
                stimulus2 = student_data.get("stimulus2")

                name_label = QLabel("Name: " + name)
                stimulus1_label = QLabel("stimulus 1: " + stimulus1)
                stimulus2_label = QLabel("stimulus 2: " + stimulus2)

                # Bar chart
                categories = ["SVREye", "GBEmotion", "RFEye", "RFFusion"]

                scores = [student_data.get("SVREye_stimulus1"), student_data.get("GBEmotion_stimulus1"),
                          student_data.get("RFEye_stimulus1"), student_data.get("RFFusion_stimulus1"),
                          student_data.get("SVREye_stimulus2"), student_data.get("GBEmotion_stimulus2"),
                          student_data.get("RFEye_stimulus2"), student_data.get("RFFusion_stimulus2")]

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
            self.main_layout.addWidget(self.report_widget)
        except Exception as e:
            print("An error occurred in update_student_data:", str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    screen = EngagementReportWidget()
    screen.setGeometry(100, 100, 1600, 1200)
    screen.show()
    sys.exit(app.exec_())
