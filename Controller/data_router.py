import os
import sys
import cv2


from pathlib import Path
from PyQt5.QtWidgets import *

video_directory = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")

from Controller import emotional_analysis
from Controller.helper import show_confirmation
from Controller.helper import read_yaml
import View.Pages.dashboard_widget as dashboard_widget
import View.Pages.instructions_widget as instructions_widget
import View.Pages.consent_form_widget as consent_form_widget
import View.Pages.presurvey_widget as pre_survey_widget
import View.Pages.start_session_widget as start_session_widget
import View.Pages.PostSurvey.post_survey_widget as post_survey_widget
import View.Pages.session_history_widget as session_history_widget
import View.Pages.engagement_report_widget as engagement_report_widget
import View.Components.bottom_button_bar as bottom_button_bar


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_layout = QVBoxLayout()
        self.screen_layout.setContentsMargins(0, 0, 0, 14)
        self.collect_data_screen_list = ["Dashboard", "Instructions", "Consent Form",
                                         "Pre Survey", "Start Session", "Post Survey"]
        self.analyze_data_screen_list = ["Dashboard", "Session History", ""]
        self.agree_checkbox = QCheckBox()
        self.main_stack_widget = QStackedWidget(self)
        self.collect_data_stacked_widget = QStackedWidget(self)
        self.analyze_data_stacked_widget = QStackedWidget(self)
        self.post_quiz_widget = None

        self.bottom_button_bar_widget = QWidget()
        self.student_data = None
        self.select_model = None

        # Initialize camera
        self.camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        # Initialize emotional analysis
        self.emotional_analysis = emotional_analysis.EmotionalAnalysis(self.camera)

        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("Quiz Application")
            self.setGeometry(100, 40, 1200, 960)
            self.setLayout(self.screen_layout)

            # Read instructions data from YAML
            instructions = read_yaml("../quiz_data/instructions.yaml")
            # Read consent form data from YAML
            consent_form = read_yaml("../quiz_data/consent_form.yaml")
            # Read pre survey data from YAML
            pre_survey = read_yaml("../quiz_data/pre_survey.yaml")
            

            # create an instance of StartPageWidget
            self.dashboard_widget = dashboard_widget.Dashboard()
            # create an instance of InstructionsWidget
            self.instructions_widget = instructions_widget.InstructionsWidget(instructions)
            # main.py
            # create an instance of ConsentFormWidget
            self.consent_form_widget = consent_form_widget.ConsentFormWidget(consent_form)
            # connect signal to the method
            self.consent_form_widget.connect_signals(self.update_start_pre_survey_button)
            # create an instance of StartSession
            self.start_session_widget = start_session_widget.StartSession(self.camera)

            # create an instance of PreSurveyWidget
            self.pre_survey_widget = pre_survey_widget.PreSurveyWidget(pre_survey)

            # manage different screens in a stacked widget
            self.collect_data_stacked_widget.addWidget(self.instructions_widget)
            self.collect_data_stacked_widget.addWidget(self.consent_form_widget)
            self.collect_data_stacked_widget.addWidget(self.pre_survey_widget)
            self.collect_data_stacked_widget.addWidget(self.start_session_widget)

            # set the initial screen
            self.collect_data_stacked_widget.setCurrentIndex(0)

            # Create an instance of the BottomButtonBar
            self.bottom_button_bar_widget = bottom_button_bar.BottomButtonBar()
            self.bottom_button_bar_widget.connect_signals(self.back_button_clicked, show_confirmation,
                                                          self.next_button_clicked)

            # analyze data branch
            # create an instance of SessionHistory Widget
            self.session_history_widget = (
                session_history_widget.SessionHistoryWidget())
            # create an instance of EngagementReport Widget
            self.engagement_report_widget = engagement_report_widget.EngagementReportWidget()
            # manage different screen in a Analyze Data stacked widget
            self.analyze_data_stacked_widget.addWidget(self.session_history_widget)  # index 0
            self.analyze_data_stacked_widget.addWidget(self.engagement_report_widget)  # index 1

            # add main stacked widget to the screen layout
            self.screen_layout.addWidget(self.main_stack_widget)

            # add root screen and branch stacked widgets to the main stacked widget
            self.main_stack_widget.addWidget(self.dashboard_widget)
            self.main_stack_widget.addWidget(self.collect_data_stacked_widget)
            self.main_stack_widget.addWidget(self.analyze_data_stacked_widget)

            # add bottom button widget to the screen layout
            self.screen_layout.addWidget(self.bottom_button_bar_widget)

            # connect button in start page widget to switch between branches
            self.dashboard_widget.collect_data_clicked.connect(lambda: self.switch_to_branch(1))
            self.dashboard_widget.analyze_data_clicked.connect(lambda: self.switch_to_branch(2))

            # connect button in session history widget
            self.session_history_widget.select_student_signal.connect(self.handle_view_report_clicked)

        except Exception as e:
            print("An error occurred in Quiz App:", str(e))

    def switch_to_branch(self, branch_index):
        self.main_stack_widget.setCurrentIndex(branch_index)
        if branch_index > 0:
            self.bottom_button_bar_widget.show()
            if branch_index == 1:
                self.bottom_button_bar_widget.set_button_info(
                    self.collect_data_screen_list[0],
                    self.collect_data_screen_list[2]
                )
            if branch_index == 2:
                self.bottom_button_bar_widget.set_next_button_enabled(False)
                self.bottom_button_bar_widget.set_button_info(
                    self.analyze_data_screen_list[0], None
                )
        else:
            self.bottom_button_bar_widget.hide()
            self.bottom_button_bar_widget.set_next_button_enabled(True)

    def back_button_clicked(self):
        try:
            if self.main_stack_widget.currentIndex() == 1:  # collect data branch
                current_index = self.collect_data_stacked_widget.currentIndex()
                # if current index is 0, switch to start screen
                if current_index == 0:
                    self.switch_to_branch(0)
                else:
                    # go to previous screen
                    self.collect_data_stacked_widget.setCurrentIndex(current_index - 1)
                    self.bottom_button_bar_widget.set_button_info(
                        self.collect_data_screen_list[current_index - 1],
                        self.collect_data_screen_list[current_index + 1]
                    )

                # if back to consent form
                if current_index == 2:
                    self.bottom_button_bar_widget.set_next_button_enabled(False)
                    self.consent_form_widget.set_checked(False)
                else:
                    self.bottom_button_bar_widget.set_next_button_enabled(True)

            # switch to analyze data branch
            if self.main_stack_widget.currentIndex() == 2:
                current_index = self.analyze_data_stacked_widget.currentIndex()
                if current_index == 0:
                    self.switch_to_branch(0)  # if current index is 0, switch to dashboard screen
                else:
                    self.analyze_data_stacked_widget.setCurrentIndex(current_index - 1)  # go to previous screen
                    self.bottom_button_bar_widget.set_button_info(
                        self.analyze_data_screen_list[current_index - 1], None
                    )

        except Exception as e:
            print("An error occurred in back_button_clicked:", str(e))

    def next_button_clicked(self):
        try:
            if self.main_stack_widget.currentIndex() == 1:  # collect data branch
                current_index = self.collect_data_stacked_widget.currentIndex()
                # go to next screen
                if current_index < self.collect_data_stacked_widget.count() - 1:
                    self.collect_data_stacked_widget.setCurrentIndex(current_index + 1)
                    self.bottom_button_bar_widget.set_button_info(
                        self.collect_data_screen_list[current_index + 1],
                        self.collect_data_screen_list[current_index + 3]
                    )

                # if going to consent form, initialize settings for consent form
                if current_index == 0:
                    self.bottom_button_bar_widget.set_next_button_enabled(False)
                    self.consent_form_widget.set_checked(False)
                else:
                    self.bottom_button_bar_widget.set_next_button_enabled(True)

                # if going to start survey
                if current_index == self.collect_data_stacked_widget.count() - 2:
                    self.start_session_widget.open_camera()

                # if going to post survey
                if current_index == self.collect_data_stacked_widget.count() - 1:
                    # self.start_session_widget.stop_camera()
                    self.bottom_button_bar_widget.hide()
                    self.post_quiz_widget = post_survey_widget.PostQuizWidget(self.emotional_analysis)
                    self.post_quiz_widget.finish_widget.go_to_dashboard_button.clicked.connect(
                        self.on_go_to_dashboard_clicked)
                    self.collect_data_stacked_widget.addWidget(self.post_quiz_widget)

                    self.collect_data_stacked_widget.setCurrentIndex(current_index + 1)

            if self.main_stack_widget.currentIndex() == 2:  # analyze data branch
                self.bottom_button_bar_widget.set_next_button_enabled(False)
                current_index = self.analyze_data_stacked_widget.currentIndex()
                # go to next screen
                if current_index < self.analyze_data_stacked_widget.count() - 1:
                    self.analyze_data_stacked_widget.setCurrentIndex(current_index + 1)

        except Exception as e:
            print("An error occurred in next_button_clicked:", str(e))

    # main.py
    def update_start_pre_survey_button(self):
        if self.consent_form_widget.get_checked():
            self.bottom_button_bar_widget.set_next_button_enabled(True)
        else:
            self.bottom_button_bar_widget.set_next_button_enabled(False)

    def handle_view_report_clicked(self, student_session_data):
        try:
            # Update data on Engagement report screen
            current_index = self.analyze_data_stacked_widget.currentIndex()
            self.analyze_data_stacked_widget.setCurrentIndex(current_index + 1)

            self.bottom_button_bar_widget.set_button_info(
                self.analyze_data_screen_list[current_index + 1], None
            )

            self.student_data = student_session_data
            self.engagement_report_widget.update_student_data(self.student_data)

        except Exception as e:
            print("An error occurred in handle_view_report_clicked:", str(e))

    def on_go_to_dashboard_clicked(self):
        # Reset screen index
        self.collect_data_stacked_widget.setCurrentIndex(0)
        self.main_stack_widget.setCurrentIndex(0)

        # Remove post quiz widget
        self.collect_data_stacked_widget.removeWidget(self.post_quiz_widget)
        self.post_quiz_widget.deleteLater()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("../styles.qss").read_text())
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
