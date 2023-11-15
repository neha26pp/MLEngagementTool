import os
import sys
import yaml
from pathlib import Path
import random
from PyQt5.QtWidgets import *

video_directory = os.path.join(os.path.dirname(__file__), "..", "View")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")

import emotional_analysis as emotional_analysis
import instructions_widget as instructions_widget
import consent_form_widget as consent_form_widget
import presurvey_widget as pre_survey_widget
import post_survey_widget as post_survey_widget


def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.agree_checkbox = None
        self.stacked_widget = QStackedWidget(self)
        self.screen_layout = QVBoxLayout()
        self.bottomButtonLayout = QHBoxLayout()
        self.bottomButtonWidget = QWidget()

        self.initUI()

    def initUI(self):
        try:
            self.setWindowTitle("Quiz Application")
            self.setGeometry(100, 100, 1400, 1000)
            self.setLayout(self.screen_layout)

            # Read instructions data from YAML
            instructions = read_yaml("../quiz_data/instructions.yaml")
            # Read consent form data from YAML
            consent_form = read_yaml("../quiz_data/consent_form.yaml")
            # Read pre survey data from YAML
            pre_survey = read_yaml("../quiz_data/pre_survey.yaml")
            # Read individual interest survey data from YAML
            individual_interest_survey = read_yaml("../quiz_data/individual_interest_questionnaire.yaml")

            self.loadMaterialQuizPairs()

            # create an instance of EmotionalAnalysis
            self.emotional_analysis = emotional_analysis.EmotionalAnalysis()
            # create an instance of InstructionsWidget
            self.instructions_widget = instructions_widget.InstructionsWidget(instructions)
            # create an instance of ConsentFormWidget
            self.consent_form_widget = consent_form_widget.ConsentFormWidget(consent_form)

            # create the 3 widgets
            self.pre_survey_widget = pre_survey_widget.PreSurveyWidget(pre_survey)
            self.post_quiz_widget = post_survey_widget.PostQuizWidget(self.display_content, self.emotional_analysis,
                                                                      type(self.display_content[0]),
                                                                      type(self.display_content[1]))

            # manage different pages in a stacked widget
            self.stacked_widget.addWidget(self.instructions_widget)
            self.stacked_widget.addWidget(self.consent_form_widget)
            self.stacked_widget.addWidget(self.pre_survey_widget)
            self.stacked_widget.addWidget(self.post_quiz_widget)

            # set the initial page
            self.stacked_widget.setCurrentIndex(0)

            # add the stacked widget to the layout
            self.screen_layout.addWidget(self.stacked_widget)

            # Create a checkbox for user agreement
            self.agree_checkbox = QCheckBox("I agree to the terms and conditions")
            self.agree_checkbox.stateChanged.connect(self.update_start_pre_survey_button)
            self.screen_layout.addWidget(self.agree_checkbox)
            self.agree_checkbox.hide()

            # add bottom button bar to the layout
            self.back_button = QPushButton("Back")
            self.back_button.setEnabled(False)
            self.back_button.setObjectName("bottomButton")
            self.back_button.clicked.connect(self.back_button_clicked)

            self.cancel_button = QPushButton("Cancel Session")
            self.cancel_button.setObjectName("bottomButton")
            self.cancel_button.clicked.connect(self.next_button_clicked)

            self.next_button = QPushButton("Next")
            self.next_button.setObjectName("bottomButton")
            self.next_button.clicked.connect(self.next_button_clicked)

            self.bottomButtonLayout.addWidget(self.back_button)
            self.bottomButtonLayout.addWidget(self.cancel_button)
            self.bottomButtonLayout.addWidget(self.next_button)
            self.bottomButtonWidget.setLayout(self.bottomButtonLayout)
            self.screen_layout.addWidget(self.bottomButtonWidget)

        except Exception as e:
            print("An error occurred in Quiz App:", str(e))

    def back_button_clicked(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)
        else:
            self.back_button.setEnabled(False)
        # if back is on consent form
        if current_index == 2:
            self.next_button.setEnabled(False)
            self.agree_checkbox.show()
            self.agree_checkbox.setChecked(False)
        else:
            if self.agree_checkbox and not self.agree_checkbox.isHidden():
                self.next_button.setEnabled(True)
                self.agree_checkbox.hide()

        if self.bottomButtonWidget.isHidden():
            self.bottomButtonWidget.show()

    def next_button_clicked(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)
            self.back_button.setEnabled(True)

        # if going to consent form
        if current_index == 0:
            self.next_button.setEnabled(False)
            self.agree_checkbox.show()
            self.agree_checkbox.setChecked(False)
        else:
            if self.agree_checkbox and not self.agree_checkbox.isHidden():
                self.next_button.setEnabled(True)
                self.agree_checkbox.hide()

        # if going to post survey hide the bottom bar
        if current_index == self.stacked_widget.count() - 2:
            self.bottomButtonWidget.hide()
            # start recording subject and performing emotional analysis
            print("starting emotional analysis")
            self.emotional_analysis.start()

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

                    # get the text and video matrial
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
        # generate a random number to determine sequence of video and text (if rand num == 1, text first; else video first)
        rand_num = random.randint(1, 2)

        if rand_num == 1:
            self.display_content.append(self.rand_text)
            self.display_content.append(self.rand_video)
        else:
            self.display_content.append(self.rand_video)
            self.display_content.append(self.rand_text)


class TextQuizPair:
    def __init__(self, material):
        self.material = material

class VideoQuizPair:
    def __init__(self, material):
        self.material = material


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("../styles.qss").read_text())
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
