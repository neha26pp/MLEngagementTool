import os
import sys
import yaml
from pathlib import Path
import random

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QTimer

video_directory = os.path.join(os.path.dirname(__file__), "..", "View")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")

import video as video
import emotional_analysis as emotional_analysis
import instructions_widget as instructions_widget
import consent_form_widget as consent_form_widget
import presurvey_widget as pre_survey_widget
import post_survey_widget as post_survey_widget

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.screen_layout = QVBoxLayout()
        self.text_pairs = None
        self.video_pairs = None
        self.display_content = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Quiz Application")
        self.setGeometry(100, 100, 1400, 400)

        # Read instructions data from YAML
        with open("../quiz_data/instructions.yaml", "r", encoding="utf-8") as yaml_file:
            instructions = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Read consent form data from YAML
        with open("../quiz_data/consent_form.yaml", "r", encoding="utf-8") as yaml_file:
            consent_form = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Read pre survey data from YAML
        with open("../quiz_data/pre_survey.yaml", "r", encoding="utf-8") as yaml_file:
            pre_survey = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Read individual interest survey data from YAML
        with open("../quiz_data/individual_interest_questionnaire.yaml", "r", encoding="utf-8") as yaml_file:
            individual_interest_survey = yaml.load(yaml_file, Loader=yaml.FullLoader)

        self.loadMaterialQuizPairs()

        # create an instance of EmotionalAnalysis
        self.emotional_analysis = emotional_analysis.EmotionalAnalysis()

        # create an instance of InstructionsWidget
        self.instructions_widget = instructions_widget.InstructionsWidget(instructions)

        # create an instance of ConsentFormWidget
        self.consent_form_widget = consent_form_widget.ConsentFormWidget(consent_form)

        # next button
        self.go_to_postquiz_button = QPushButton("Next")

        # create the 3 widgets
        self.pre_survey_widget = pre_survey_widget.PreSurveyWidget(pre_survey)
        self.post_quiz_widget = post_survey_widget.PostQuizWidget(self.display_content, self.emotional_analysis, type(self.display_content[0]), type(self.display_content[1]))
       

        # show instructions page
        self.screen_layout.addWidget(self.instructions_widget)
        self.instructions_widget.show()
        self.setLayout(self.screen_layout)

        # add a Next button
        self.go_to_consent_form_button = QPushButton("Next")
        self.screen_layout.addWidget(self.go_to_consent_form_button)
        self.go_to_consent_form_button.clicked.connect(self.transition_to_consent_form)

    def update_start_pre_survey_button(self ):
        if self.agree_checkbox.isChecked():
            self.start_pre_survey_button.setEnabled(True)
        else:
            self.start_pre_survey_button.setEnabled(False)

    def transition_to_consent_form(self):
        # remove instructions widgets
        self.screen_layout.removeWidget(self.instructions_widget)
        self.instructions_widget.deleteLater()

        # remove next button
        self.screen_layout.removeWidget(self.go_to_consent_form_button)
        self.go_to_consent_form_button.deleteLater()

        # show consent form
        self.screen_layout.addWidget(self.consent_form_widget)
        self.consent_form_widget.show()
        self.setLayout(self.screen_layout)

        # Create a checkbox for user agreement
        self.agree_checkbox = QCheckBox("I agree to the terms and conditions")
        self.agree_checkbox.stateChanged.connect(self.update_start_pre_survey_button)
        self.screen_layout.addWidget(self.agree_checkbox)

        # add a Start Pre-survey button 
        self.start_pre_survey_button = QPushButton("Start Pre-survey")
        self.start_pre_survey_button.setEnabled(False)
        self.screen_layout.addWidget(self.start_pre_survey_button)
        self.start_pre_survey_button.clicked.connect(self.transition_to_pre_survey)

    def transition_to_pre_survey(self):
        # remove consent form widgets
        self.screen_layout.removeWidget(self.consent_form_widget)
        self.consent_form_widget.deleteLater()

        self.screen_layout.removeWidget(self.agree_checkbox)
        self.agree_checkbox.deleteLater()

        # remove next button
        self.screen_layout.removeWidget(self.start_pre_survey_button)
        self.start_pre_survey_button.deleteLater()

        # add pre_survey widgets
        self.screen_layout.addWidget(self.pre_survey_widget)
        # show pre_survey
        self.pre_survey_widget.show()

        # add next button
        self.screen_layout.addWidget(self.go_to_postquiz_button)
        self.go_to_postquiz_button.clicked.connect(self.transition_to_post_quiz)


    def transition_to_post_quiz(self):

        # remove pre-survey widgets
        self.screen_layout.removeWidget(self.pre_survey_widget)
        self.pre_survey_widget.deleteLater()

        # remove next button
        self.screen_layout.removeWidget(self.go_to_postquiz_button)
        self.go_to_postquiz_button.deleteLater()

        # start recording subject and performing emotional analysis
        print("starting emotional analysis")
        self.emotional_analysis.start()
       
        # add post_quiz widgets
        self.screen_layout.addWidget(self.post_quiz_widget)
        # show post_quiz
        self.post_quiz_widget.show()

       

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
                if (
                    os.path.exists(material_path)
                    and os.path.exists(text_quiz_path)
                    and os.path.exists(video_quiz_path)
                ):
                    # Read the contents of material and text quiz and video quiz files
                    with open(material_path, "r", encoding="utf-8") as material_file:
                        material_data = yaml.load(material_file, Loader=yaml.FullLoader)

                    # get the text and video matrial
                    self.text_pairs = TextQuizPair(material_data)
                    self.texts.append(self.text_pairs)
                  
                    # Create a VideoQuizPair instance and append to the list
                    self.video_pairs = VideoQuizPair(material_data)
                    self.videos.append(self.video_pairs)
                else:
                    print("something's wrong")

        # randomly pick a text
        self.rand_text = random.choice(self.texts)
        # print the index of self.rand_text
        index = self.texts.index(self.rand_text)

        # remove the element at index from videos (to not pick the video belonging to same topic)
        self.videos.remove(self.videos[index]) # remove the picked text from the list so that it's corresponding video cannot be picked
        
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