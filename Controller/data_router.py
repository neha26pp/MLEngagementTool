import os
import sys
import yaml
from pathlib import Path
import random

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

video_directory = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")

import Controller.emotional_analysis as emotional_analysis
import View.instructions_widget as instructions_widget
import View.consent_form_widget as consent_form_widget
import View.presurvey_widget as pre_survey_widget
import View.post_survey_widget as post_survey_widget
import View.start_page_widget as start_page_widget
import View.start_recording_widget as start_recording_widget
import View.session_history_widget as session_history_widget
import View.select_model_widget as select_model_widget
import View.engagement_report_widget as engagement_report_widget

BOTTOM_BUTTON_H = 60  # bottom button bar height


def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


class QuizApp(QWidget):
    student_data_updated_signal = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.agree_checkbox = QCheckBox()
        self.main_stack_widget = QStackedWidget(self)
        self.collect_data_stacked_widget = QStackedWidget(self)
        self.analyze_data_stacked_widget = QStackedWidget(self)
        self.screen_layout = QVBoxLayout()
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonWidget = QWidget()

        self.student_data = None
        self.selected_model = None

        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("Quiz Application")
            self.setGeometry(100, 100, 1800, 1200)
            self.setLayout(self.screen_layout)

            # Read instructions data from YAML
            instructions = read_yaml("../quiz_data/instructions.yaml")
            # Read consent form data from YAML
            consent_form = read_yaml("../quiz_data/consent_form.yaml")
            # Read pre survey data from YAML
            pre_survey = read_yaml("../quiz_data/pre_survey.yaml")
            # Read student data from YAML
            self.session_history = read_yaml("../quiz_data/session_history.yaml")

            self.loadMaterialQuizPairs()

            # create an instance of EmotionalAnalysis
            self.emotional_analysis = emotional_analysis.EmotionalAnalysis()

            # create eye tracking thread
            # self.eye_tracker = eye_tracker.EmotionalAnalysis()

            # create an instance of StartPageWidget
            self.start_page_widget = start_page_widget.StartPage()
            # create an instance of StartRecording
            self.start_recording_widget = start_recording_widget.StartRecording()
            # create an instance of InstructionsWidget
            self.instructions_widget = instructions_widget.InstructionsWidget(instructions)
            # create an instance of ConsentFormWidget
            self.consent_form_widget = consent_form_widget.ConsentFormWidget(consent_form)

            # create the 3 widgets
            self.pre_survey_widget = pre_survey_widget.PreSurveyWidget(pre_survey)
            self.post_quiz_widget = post_survey_widget.PostQuizWidget(self.display_content, self.emotional_analysis,
                                                                      self.display_content[0].text,
                                                                      self.display_content[1].text)

            # manage different screens in a stacked widget
            self.collect_data_stacked_widget.addWidget(self.instructions_widget)
            self.collect_data_stacked_widget.addWidget(self.consent_form_widget)
            self.collect_data_stacked_widget.addWidget(self.pre_survey_widget)
            self.collect_data_stacked_widget.addWidget(self.start_recording_widget)
            self.collect_data_stacked_widget.addWidget(self.post_quiz_widget)

            # set the initial screen
            self.collect_data_stacked_widget.setCurrentIndex(0)

            # Create bottom button bar
            self.back_button = QPushButton("Back")
            self.back_button.setObjectName("bottomButton")
            self.back_button.setFixedHeight(BOTTOM_BUTTON_H)
            self.back_button.clicked.connect(self.back_button_clicked)

            self.cancel_button = QPushButton("Cancel Session")
            self.cancel_button.setObjectName("bottomButton")
            self.cancel_button.setFixedHeight(BOTTOM_BUTTON_H)
            self.cancel_button.clicked.connect(self.showConfirmation)

            self.next_button = QPushButton("Next")
            self.next_button.setObjectName("bottomButton")
            self.next_button.setFixedHeight(BOTTOM_BUTTON_H)
            self.next_button.clicked.connect(self.next_button_clicked)

            self.bottomButtonLayout.addWidget(self.back_button)
            self.bottomButtonLayout.addWidget(self.cancel_button)
            self.bottomButtonLayout.addWidget(self.next_button)
            self.bottomButtonWidget.setLayout(self.bottomButtonLayout)
            self.bottomButtonWidget.hide()

            # analyze data branch
            # create an instance of SessionHistory Widget
            self.session_history_widget = (
                session_history_widget.SessionHistoryWidget(session_history=self.session_history))
            # create an instance of SelectModel Widget
            # create an instance of SelectModel Widget
            self.select_model_widget = select_model_widget.SelectModelWidget()
            # create an instance of EngagementReport Widget
            self.engagement_report_widget = (engagement_report_widget.EngagementReportWidget(
                student_data=self.student_data, model=self.selected_model))
            # manage different screen in a Analyze Data stacked widget
            self.analyze_data_stacked_widget.addWidget(self.session_history_widget)  # index 0
            self.analyze_data_stacked_widget.addWidget(self.select_model_widget)  # index 1
            self.analyze_data_stacked_widget.addWidget(self.engagement_report_widget)  # index 2

            # add main stacked widget to the screen layout
            self.screen_layout.addWidget(self.main_stack_widget)

            # add root screen and branch stacked widgets to the main stacked widget
            self.main_stack_widget.addWidget(self.start_page_widget)
            self.main_stack_widget.addWidget(self.collect_data_stacked_widget)
            self.main_stack_widget.addWidget(self.analyze_data_stacked_widget)

            # Create a checkbox for user agreement
            self.agree_checkbox = QCheckBox("I agree to the terms and conditions")
            self.agree_checkbox.stateChanged.connect(self.update_start_pre_survey_button)
            self.agree_checkbox.hide()
            self.screen_layout.addWidget(self.agree_checkbox)

            # add bottom button widget to the screen layout
            self.screen_layout.addWidget(self.bottomButtonWidget)

            # connect button in start page widget to switch between branches
            self.start_page_widget.collect_data_clicked.connect(lambda: self.switch_to_branch(1))
            self.start_page_widget.analyze_data_clicked.connect(lambda: self.switch_to_branch(2))

            # connect button in session history widget
            self.session_history_widget.view_report_clicked.connect(self.handle_view_report_clicked)
            # connect button in select model widget
            self.select_model_widget.model_selected.connect(self.handle_model_selected)
            # connect signal from QuizApp to EngagementReportWidget
            self.student_data_updated_signal.connect(self.engagement_report_widget.update_student_data)

        except Exception as e:
            print("An error occurred in Quiz App:", str(e))

    def switch_to_branch(self, branch_index):
        self.main_stack_widget.setCurrentIndex(branch_index)
        if branch_index > 0:
            self.bottomButtonWidget.show()
            if branch_index == 2:
                self.next_button.setEnabled(False)
        else:
            self.bottomButtonWidget.hide()
            self.next_button.setEnabled(True)

    def back_button_clicked(self):
        try:
            if self.main_stack_widget.currentIndex() == 1:  # collect data branch
                current_index = self.collect_data_stacked_widget.currentIndex()
                # if current index is 0, switch to start screen
                if current_index == 0:
                    self.switch_to_branch(0)
                else:  # go to previous screen
                    self.collect_data_stacked_widget.setCurrentIndex(current_index - 1)

                # if back to consent form
                if current_index == 2:
                    self.next_button.setEnabled(False)
                    self.agree_checkbox.show()
                    self.agree_checkbox.show()
                    self.agree_checkbox.setChecked(False)
                else:
                    if self.agree_checkbox and not self.agree_checkbox.isHidden():
                        self.next_button.setEnabled(True)
                        self.agree_checkbox.hide()
            if self.main_stack_widget.currentIndex() == 2:  # analyze data branch
                current_index = self.analyze_data_stacked_widget.currentIndex()
                # if current index is 0, switch to start screen
                if current_index == 0:
                    self.switch_to_branch(0)
                else:  # go to previous screen
                    self.analyze_data_stacked_widget.setCurrentIndex(current_index - 1)
                    if current_index == 1:
                        self.next_button.setEnabled(False)

        except Exception as e:
            print("An error occurred in back_button_clicked:", str(e))

    def next_button_clicked(self):
        if self.main_stack_widget.currentIndex() == 1:  # collect data branch
            current_index = self.collect_data_stacked_widget.currentIndex()
            # go to next screen
            if current_index < self.collect_data_stacked_widget.count() - 1:
                self.collect_data_stacked_widget.setCurrentIndex(current_index + 1)
                self.back_button.setEnabled(True)

            # if going to consent form, initialize settings for consent form
            if current_index == 0:
                self.next_button.setEnabled(False)
                self.agree_checkbox.show()
                self.agree_checkbox.setChecked(False)
            else:
                if self.agree_checkbox and not self.agree_checkbox.isHidden():
                    self.next_button.setEnabled(True)
                    self.agree_checkbox.hide()

            # if going to post survey
            if current_index == self.collect_data_stacked_widget.count() - 2:
                self.start_recording_widget.stop_camera()
                # print("starting eyetracking before stimulus")
                # self.eye_tracker.start()
                # print("starting emotional analysis before stimulus")
                # self.emotional_analysis.start()
        if self.main_stack_widget.currentIndex() == 2:  # analyze data branch
            current_index = self.analyze_data_stacked_widget.currentIndex()
            self.next_button.setEnabled(False)
            # go to next screen
            if current_index < self.analyze_data_stacked_widget.count() - 1:
                self.analyze_data_stacked_widget.setCurrentIndex(current_index + 1)
                self.back_button.setEnabled(True)
            if current_index == 1:
                # emit signal when moving to engagement report
                self.student_data_updated_signal.emit(self.student_data)

    def update_start_pre_survey_button(self):
        if self.agree_checkbox.isChecked():
            self.next_button.setEnabled(True)
        else:
            self.next_button.setEnabled(False)

    def loadMaterialQuizPairs(self):
        # Directory where subdirectories containing material and quiz files are located
        directory = "../quiz_data/post_quiz"  # Update to your directory path

        # Initialize an empty list to store texts and videos
        self.texts = []
        self.videos = []

        self.display_content = []

        # Iterate through the subdirectories
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)

            # Check if it's a directory
            if os.path.isdir(subdir_path):
                material_path = os.path.join(subdir_path, "material.yaml")
                text_quiz_path = os.path.join(subdir_path, "text_quiz.yaml")
                video_quiz_path = os.path.join(subdir_path, "video_quiz.yaml")

                # Check if both material and quiz files exist in the subdirectory
                if os.path.exists(material_path) and os.path.exists(text_quiz_path) and os.path.exists(video_quiz_path):
                    # Read the contents of material and text quiz and video quiz files
                    material_data = read_yaml(material_path)

                    # get the text and video material
                    self.text_pairs = TextQuizPair(material_data)
                    self.texts.append(self.text_pairs)

                    # Create a VideoQuizPair instance and append to the list
                    self.video_pairs = VideoQuizPair(material_data)
                    self.videos.append(self.video_pairs)
                else:
                    print("error occurs in loadMaterialQuizPairs")

        # randomly pick a text
        self.rand_text = random.choice(self.texts)
        # print the index of self.rand_text
        index = self.texts.index(self.rand_text)

        # remove the element at index from videos (to not pick the video belonging to same topic)
        self.videos.remove(self.videos[
                               index])  # remove the picked text from the list so that it's corresponding video cannot be picked

        # pick video from other topic
        self.rand_video = self.videos[0]
        # generate a random number to determine sequence of video and text
        # (if rand num == 1, text first; else video first)
        rand_num = random.randint(1, 2)

        if rand_num == 1:
            self.display_content.append(self.rand_text)
            self.display_content.append(self.rand_video)
            print("display_content:", self.display_content)
        else:
            self.display_content.append(self.rand_video)
            self.display_content.append(self.rand_text)
            print("display_content:", self.display_content)

    def handle_view_report_clicked(self, row):
        try:
            current_index = self.analyze_data_stacked_widget.currentIndex()
            self.analyze_data_stacked_widget.setCurrentIndex(current_index + 1)
            self.student_data = self.session_history[row]
            print("handle_view_report_clicked:", self.student_data)
            self.engagement_report_widget.update_student_data(self.student_data)
        except Exception as e:
            print("An error occurred in handle_view_report_clicked:", str(e))

    def handle_model_selected(self, selected_radio):
        self.selected_model = selected_radio
        self.next_button.setEnabled(True)

    def showConfirmation(self):
        # create message box
        reply = QMessageBox.question(self, 'Confirmation', 'Are you sure you want to exit?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        # process confirmation
        if reply == QMessageBox.Yes:
            # if yes, exit the system
            sys.exit()
        else:
            # if no, cancel exit
            pass


class TextQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = True


class VideoQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("../styles.qss").read_text())
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
