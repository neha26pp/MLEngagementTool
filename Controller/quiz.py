import os
import sys
import yaml
from pathlib import Path
import random

from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWebEngineWidgets


video_directory = os.path.join(os.path.dirname(__file__), "..", "View")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")
import video as video
import emotional_analysis as emotional_analysis



class PreSurveyWidget(QWidget):
    def __init__(self, pre_survey, parent=None):
        super().__init__(parent)
        self.pre_survey = pre_survey
        self.screen_layout = QVBoxLayout()
        self.emotional_analysis = emotional_analysis
        # radio button
        self.buttonGroups = []  # for radio button groups
        self.question_grid_layout = QGridLayout()
        self.radio_group = QButtonGroup(self)

        self.initUI()

    def initUI(self):
        # Create a label for "Pre Survey" heading
        pre_survey_heading = QLabel("Pre Survey")
        pre_survey_heading.setObjectName("heading1")
        pre_survey_heading.setFixedHeight(75)
        self.screen_layout.addWidget(pre_survey_heading)

        # Create a grid layout for personal information form
        info_grid_layout = QGridLayout()
        for i, info in enumerate(self.pre_survey.get("information_form")):
            info_form_layout = QFormLayout()
            info_label = QLabel(info)
            info_input = QLineEdit()
            info_label.setFixedWidth(120 if i % 3 < 2 else 250)
            info_input.setFixedWidth(125)
            info_form_layout.addRow(info_label, info_input)
            info_grid_layout.addItem(info_form_layout, int(i / 3), i % 3)
        info_grid_layout.setColumnStretch(0, 1)
        info_grid_layout.setColumnStretch(1, 1)
        info_grid_layout.setColumnStretch(2, 2)
        info_grid_widget = QWidget()
        info_grid_widget.setLayout(info_grid_layout)
        info_grid_widget.setFixedHeight(100)
        self.screen_layout.addWidget(info_grid_widget)

        # Create a grid layout for personal information question table
        head_grid_layout = QGridLayout()
        head_grid_layout.setColumnStretch(0, 1)
        head_grid_layout.setColumnStretch(1, 2)
        for i, label_text in enumerate(["Questions", "Scale Ratings"]):
            head_question_label = QLabel(label_text)
            head_question_label.setObjectName("headGridWidget")
            head_grid_layout.addWidget(head_question_label, 0, i)

        # Create a grid layout for scale ratings
        scale_rating_grid_layout = QGridLayout()
        option_list = [
            "strongly agree",
            "agree",
            "neither",
            "disagree",
            "strongly disagree",
        ]
        for i, option in enumerate(option_list):
            option_label = QLabel(option)
            option_label.setObjectName("headGridWidget")
            scale_rating_grid_layout.addWidget(option_label, 0, i)

        # Add scale ratings to head grid layout
        head_grid_layout.addItem(scale_rating_grid_layout, 1, 1)
        head_grid_widget = QWidget()
        head_grid_widget.setObjectName("headGridWidget")
        head_grid_widget.setLayout(head_grid_layout)
        head_grid_widget.setFixedHeight(75)
        self.screen_layout.addWidget(head_grid_widget)

        # Show Likert Scale questions
        for question_i, question in enumerate(self.pre_survey.get("questions")):
            self.show_scale_questions(question_i, question)

        # Fix column stretch
        self.question_grid_layout.setColumnStretch(0, 1)
        self.question_grid_layout.setColumnStretch(1, 2)

        # Set layouts
        self.screen_layout.addItem(self.question_grid_layout)
        self.setLayout(self.screen_layout)

    def show_scale_questions(self, question_i, question):
        # Create a QLabel for the question text and set it to word wrap
        question_label = QLabel(question.get("text"))
        question_label.setWordWrap(True)
        self.question_grid_layout.addWidget(question_label, question_i, 0)
        # Check if it's a scale question with subtext
        if question.get("type") == "scale" and question.get("hasSubtext"):
            for sub_question_i, text in enumerate(question.get("subtext")):
                # Create QLabel for subtext, set it to word wrap, and add it to the layout
                question_label = QLabel(text)
                question_label.setWordWrap(True)
                self.question_grid_layout.addWidget(
                    question_label, question_i + sub_question_i + 1, 0
                )
                # Show scale options for subtext questions
                self.show_scale_options(question_i + sub_question_i + 1)
        # Check if it's a regular scale question
        elif question.get("type") == "scale":
            # Show scale options for the question
            self.show_scale_options(question_i)

    def show_scale_options(self, question_i):
        # Create a button group for radio buttons
        radio_group = QButtonGroup(self)
        layout_scale_option = QGridLayout()
        # Create radio buttons
        for radio_button_i in range(5):
            radio_button = QRadioButton()
            radio_group.addButton(radio_button, radio_button_i)
            layout_scale_option.addWidget(radio_button, 0, radio_button_i)
        # Add the layout with radio buttons to the main question grid layout
        self.question_grid_layout.addLayout(layout_scale_option, question_i, 1)
        # Append the radio button group to a list for future reference
        self.buttonGroups.append(radio_group)

    def get_answers(self):  ##########
        # Get answers from personal information widgets
        information_answers = [info_input.text() for info_input in self.findChildren(QLineEdit)]
    
        # Get the selected radio button options for scale questions
        selected_options = []
        for radio_group in self.buttonGroups:
            selected_option = radio_group.checkedId()
            if selected_option != -1:
                selected_options.append(selected_option)

        responses = information_answers + selected_options
         # Save responses to a file
        with open(file_path, "a") as file:
            file.write("Pre Survey Responses:\n")
            for response in responses:
                file.write(str(response) + "\n")

        # Print a message indicating that the responses have been saved
        print("Responses saved to file:", file_path)

        return responses
        


class PostQuizWidget(QWidget):
    def __init__(self, display_content, emotional_analysis, parent=None):
        super().__init__(parent)
        # read data
        self.emotional_analysis = emotional_analysis
        self.display_content = display_content

        # initialize layouts
        self.question_grid_widget = QWidget()
        self.question_grid_layout = QGridLayout()
        self.screen_layout = QVBoxLayout()

        # initialize index
        self.current_question = 0
        self.current_material = 0
        self.buttonGroups = [] # for radio button groups

        self.initUI()

    def initUI(self):
        try:
            self.setLayout(self.screen_layout)
            self.go_to_next_material()

        except Exception as e:
            print("An error occurred:", str(e))

    def go_to_next_material(self):
        if self.current_material < len(self.display_content):
            # display content has either [video, text] or [text, video]

            if type(self.display_content[self.current_material]) is TextQuizPair:
                self.reading_text = self.display_content[
                    self.current_material
                ].material.get("reading-text")
                self.post_quiz = self.display_content[self.current_material].quiz
                self.show_reading_material()
            else:
                self.video_button = QPushButton("Watch Video")
                self.screen_layout.addWidget(self.video_button)
                self.video_button.clicked.connect(self.show_video)
                self.reading_text =  self.display_content[self.current_material].material.get("reading-text")
                self.video_url = (
                    self.display_content[self.current_material]
                    .material.get("reading-text")
                    .get("video")
                )
                self.post_quiz = self.display_content[self.current_material].quiz

            self.current_material += 1

        else:
            self.show_completed_message()

    def show_reading_material(self):
        # Initialize reading text widget
        self.reading_text_widget = QScrollArea()
        # self.reading_text_widget.setStyleSheet("background: lightblue") # Debugging
        self.reading_text_widget.setWidgetResizable(True)
        # Set reading text heading
        self.reading_text_heading = QLabel("Reading Text")
        self.reading_text_heading.setObjectName("heading1")
        self.reading_text_heading.setFixedHeight(75)
        self.screen_layout.addWidget(self.reading_text_heading)

        self.reading_topic = QLabel(self.reading_text.get("topic"))

        # Show reading topic if available
        if self.reading_topic != "":
            self.reading_topic.setObjectName("heading2")
            self.screen_layout.addWidget(self.reading_topic)

        # Show reading text content
        self.reading_text_label = QLabel(" ".join(self.reading_text.get("text")))
        self.reading_text_label.setWordWrap(True)
        self.reading_text_widget.setWidget(self.reading_text_label)

        # Add reading material widget to screen layout
        self.screen_layout.addWidget(self.reading_text_widget)
        self.webview = None

        # Set start quiz button
        self.start_quiz_button = QPushButton("Start Quiz")
        self.screen_layout.addWidget(self.start_quiz_button)
        self.start_quiz_button.clicked.connect(self.go_to_next_question)

    def show_video(self):
        try:
            print("in video function")
            # Get video URL

            if self.video_button:
                self.video_button.deleteLater()
                self.screen_layout.removeWidget(self.video_button)

            self.reading_text_widget = QScrollArea()
            # self.reading_text_widget.setStyleSheet("background: lightblue") # Debugging
            self.reading_text_widget.setWidgetResizable(True)
            # Set reading text heading
            self.reading_text_heading = QLabel("Video")
            self.reading_text_heading.setObjectName("heading1")
            self.reading_text_heading.setFixedHeight(75)
            self.screen_layout.addWidget(self.reading_text_heading)

            self.reading_topic = QLabel(self.reading_text.get("topic"))

            # Show reading topic if available
            # if self.reading_topic != "":
            # self.reading_topic.setObjectName("heading2")
            # self.screen_layout.addWidget(self.reading_topic)
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.video_url))
            self.screen_layout.addWidget(self.webview)
            # Set start quiz button
            self.start_quiz_button = QPushButton("Start Quiz")
            self.screen_layout.addWidget(self.start_quiz_button)
            self.start_quiz_button.clicked.connect(self.go_to_next_question)

        except Exception as e:
            print("An error occurred in video func:", str(e))

    def go_to_next_question(self):
        try:
            if self.start_quiz_button:
                print("start quiz clicked")

                

                # Delete reading text widgets
                if self.reading_text_widget:
                    print("deleting reading_text_widget")
                    self.reading_text_widget.deleteLater()
                    self.screen_layout.removeWidget(self.reading_text_heading)
                    self.reading_text_heading.deleteLater()
                    self.screen_layout.removeWidget(self.reading_topic)
                    self.reading_topic.deleteLater()

                if self.webview:
                    print("deleting video webview")
                    self.webview.deleteLater()
                    self.screen_layout.removeWidget(self.webview)

                # Delete start quiz button
                self.screen_layout.removeWidget(self.start_quiz_button)
                self.start_quiz_button.deleteLater()
                self.start_quiz_button = None

                # Add post quiz heading
                self.post_quiz_heading = QLabel("Post Quiz")
                self.post_quiz_heading.setObjectName("heading1")
                self.post_quiz_heading.setFixedHeight(75)
                self.screen_layout.addWidget(self.post_quiz_heading)
            else:
                responses = self.get_answers()
                # Remove post quiz widgets
                self.screen_layout.removeWidget(self.post_quiz_widget)
                self.post_quiz_widget.deleteLater()
                # Remove next button
                self.screen_layout.removeWidget(self.submit_button)
                self.submit_button.deleteLater()

            # Initialize post quiz widget (excluding heading and next button)
            self.post_quiz_widget = QWidget()
            self.post_quiz_layout = QVBoxLayout()
            self.post_quiz_widget.setLayout(self.post_quiz_layout)
            self.screen_layout.addWidget(self.post_quiz_widget)
            # self.post_quiz_widget.setStyleSheet("background: lightblue")  # Debugging

            # Get questions data
            
            if self.current_question < len(self.post_quiz):
                # Show the current question
                self.question = self.post_quiz[self.current_question]
                self.show_question()
                # Update question index
                self.current_question += 1
                # Set next button
                self.submit_button = QPushButton("Next")
                self.screen_layout.addWidget(self.submit_button)
                self.submit_button.clicked.connect(self.go_to_next_question)
            else:
                self.current_question = 0
                self.screen_layout.removeWidget(self.post_quiz_widget)
                self.post_quiz_widget.deleteLater()
                self.screen_layout.removeWidget(self.post_quiz_heading)
                self.post_quiz_heading.deleteLater()
                self.go_to_next_material()
                return
        except Exception as e:
            print("An error occurred in go to next question:", str(e))

    def show_question(self):
        try:
            if self.question.get("type") == "scale":
                # Set heading for scale questions
                heading_label = QLabel(
                    "Based on your experience in reading the text - (strongly agree/agree/neither/disagree/strongly disagree)"
                )
                self.post_quiz_layout.addWidget(heading_label)

                # Display table for scale questions
                head_grid_layout = QGridLayout()
                head_grid_layout.setColumnStretch(0, 1)
                head_grid_layout.setColumnStretch(1, 2)

                # Set question head
                head_question_label = QLabel("Questions")
                head_question_label.setObjectName("headGridWidget")
                head_grid_layout.addWidget(head_question_label, 0, 0)

                # Set scale ratings head
                head_question_label = QLabel("Scale Ratings")
                head_question_label.setObjectName("headGridWidget")
                head_grid_layout.addWidget(head_question_label, 0, 1)

                # Display scale rating labels
                scale_rating_grid_layout = QGridLayout()
                option_list = [
                    "strongly agree",
                    "agree",
                    "neither",
                    "disagree",
                    "strongly disagree",
                ]
                for i, option in enumerate(option_list):
                    option_label = QLabel(option)
                    option_label.setObjectName("headGridWidget")
                    scale_rating_grid_layout.addWidget(option_label, 0, i)
                head_grid_layout.addItem(scale_rating_grid_layout, 1, 1)

                head_grid_widget = QWidget()
                head_grid_widget.setObjectName("headGridWidget")
                head_grid_widget.setLayout(head_grid_layout)
                head_grid_widget.setFixedHeight(75)
                self.post_quiz_layout.addWidget(head_grid_widget)

                # Fix the column stretch
                self.question_grid_layout.setColumnStretch(0, 1)
                self.question_grid_layout.setColumnStretch(1, 2)

                # Show Likert Scale questions
                for question_i, question in enumerate(self.post_quiz):
                    self.show_scale_questions(question_i, question)
            else:
                # Set heading for non-scale questions
                heading_label = QLabel("Based on the topic of the presented text")
                self.post_quiz_layout.addWidget(heading_label)

            if self.question.get("text") != "":
                # Show question text
                question_label = QLabel(self.question.get("text"))
                self.post_quiz_layout.addWidget(question_label)

            if self.question["type"] == "single":
                self.show_single_choice_options()  # Show single choice options
            if self.question["type"] == "multiple":
                self.show_multiple_choice_options()  # Show multiple choice options

        except Exception as e:
            print("An error occurred:", str(e))

    def show_single_choice_options(self):
        try:
            radio_group = QButtonGroup()
            for i, option in enumerate(self.question.get("options")):
                radio_button = QRadioButton(option)
                self.post_quiz_layout.addWidget(radio_button)
                radio_group.addButton(radio_button, i)
        except Exception as e:
            print("An error occurred:", str(e))

    def show_multiple_choice_options(self):
        for i, option in enumerate(self.question.get("options")):
            checkbox = QCheckBox(option)
            self.post_quiz_layout.addWidget(checkbox)

    def show_scale_questions(self, question_i, question):
        if question.get("hasSubtext"):
            for sub_question_i, subtext in enumerate(question.get("subtext")):
                # Create label for subtext
                question_label = QLabel(subtext)
                question_label.setWordWrap(True)

                # Add label to the question grid layout
                self.question_grid_layout.addWidget(
                    question_label, sub_question_i + question_i, 0
                )
                self.question_grid_widget.setLayout(self.question_grid_layout)
                self.post_quiz_layout.addWidget(self.question_grid_widget)

                # Show options
                self.show_scale_options(sub_question_i + question_i)
        else:
            # Show options
            self.show_scale_options(question_i)

    def show_scale_options(self, question_i):
        # Define the scale options
        option_list = [
            "strongly agree",
            "agree",
            "neither",
            "disagree",
            "strongly disagree",
        ]
        radio_group = QButtonGroup(self)  # Create a button group for radio buttons
        layout_scale_option = QGridLayout()  # Create a grid layout for scale options

        for radio_button_i, _ in enumerate(option_list):
            radio_button = QRadioButton()  # Create a radio button for the option
            radio_group.addButton(
                radio_button, radio_button_i
            )  # Add button to button group
            layout_scale_option.addWidget(
                radio_button, 0, radio_button_i
            )  # Add button to grid layout

        # Add the scale options layout to the question grid layout
        self.question_grid_layout.addLayout(layout_scale_option, question_i, 1)
        self.buttonGroups.append(
            radio_group
        )  # Append the button group to a list for later access

    def show_completed_message(self):
        # stop recording subject and performing emotional analysis
        self.emotional_analysis.stop() 
        print("Emotions detected throughout session: " ,self.emotional_analysis.detected_emotions)


        for i in reversed(range(self.post_quiz_layout.count())):
            self.post_quiz_layout.itemAt(i).widget().deleteLater()

        self.completed_label = QLabel("Post Quiz Completed!")
        self.screen_layout.addWidget(self.completed_label)

    def get_answers(self):  ##########
        # Get answers from personal information widgets
         # Collect answers from personal information widgets (text input fields)
        information_answers = [info_input.text() for info_input in self.findChildren(QLineEdit)]

        # Collect the selected radio button options for scale questions
        selected_options = []
        for radio_group in self.buttonGroups:
            selected_option = radio_group.checkedId()
            if selected_option != -1:
                selected_options.append(selected_option)

        checkbox_responses = []
        for checkbox in self.findChildren(QCheckBox):
            if checkbox.isChecked():
                checkbox_responses.append(checkbox.text())

        selected_radio_response = None
        for radio_button in self.findChildren(QRadioButton):
            if radio_button.isChecked():
                selected_radio_response = radio_button.text()
                break  # Exit the loop after finding the selected radio response

        # Combine all the responses
        responses = information_answers + selected_options + checkbox_responses + [selected_radio_response]

        # Save responses to a file
        with open(file_path, "a") as file:
            file.write("Post Quiz Responses:\n")
            for response in responses:
                file.write(str(response) + "\n")

        # Print a message indicating that the responses have been saved
        print("Responses saved to file:", file_path)

        return responses
        


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

        # Read pre survey data from YAML
        with open("../quiz_data/pre_survey.yaml", "r", encoding="utf-8") as yaml_file:
            pre_survey = yaml.load(yaml_file, Loader=yaml.FullLoader)

        self.loadMaterialQuizPairs()

        # create an instance of EmotionalAnalysis
        self.emotional_analysis = emotional_analysis.EmotionalAnalysis()

        # pass data to pre survey and post quiz
        self.pre_survey_widget = PreSurveyWidget(pre_survey)
        print(type(self.pre_survey_widget))

        self.post_quiz_widget = PostQuizWidget(self.display_content, self.emotional_analysis)

        # show pre-survey
        self.screen_layout.addWidget(self.pre_survey_widget)
        self.setLayout(self.screen_layout)
        # add next button
        self.submit_button = QPushButton("Next")
        self.screen_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.transition_to_post_quiz)

    def transition_to_post_quiz(self):

        responses = self.pre_survey_widget.get_answers()
        # remove pre-survey widgets
        self.screen_layout.removeWidget(self.pre_survey_widget)
        self.pre_survey_widget.deleteLater()

        # remove next button
        self.screen_layout.removeWidget(self.submit_button)
        self.submit_button.deleteLater()

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

        # Initialize an empty list to store MaterialQuizPair instances
        self.text_pairs = []
        self.video_pairs = []

        self.display_content = []

        # Iterate through the subdirectories
        for subdir in os.listdir(directory):
            subdir_path = os.path.join(directory, subdir)
            print(subdir_path)
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
                    with open(text_quiz_path, "r", encoding="utf-8") as quiz_file:
                        text_quiz_data = yaml.load(quiz_file, Loader=yaml.FullLoader)
                    with open(video_quiz_path, "r", encoding="utf-8") as quiz_file:
                        video_quiz_data = yaml.load(quiz_file, Loader=yaml.FullLoader)

                    # Create a TextQuizPair instance and append to the list

                    self.text_pair = TextQuizPair(material_data, text_quiz_data)
                    self.text_pairs.append(self.text_pair)
                    print("PAIRS ---", self.text_pairs)

                    # Create a VideoQuizPair instance and append to the list
                    self.video_pair = VideoQuizPair(material_data, video_quiz_data)
                    self.video_pairs.append(self.video_pair)
                else:
                    print("something's wrong")

        # randomly pick a text from text_pairs
        self.rand_text = random.choice(self.text_pairs)
        # randomly pick a video from video_pairs
        self.rand_video = random.choice(self.video_pairs)

        # generate a random number to determine sequence of video and text (if rand num == 1, text first; else video first)
        rand_num = random.randint(1, 2)
        print(rand_num)
        if rand_num == 1:
            self.display_content.append(self.rand_text)
            self.display_content.append(self.rand_video)
        else:
            self.display_content.append(self.rand_video)
            self.display_content.append(self.rand_text)


class TextQuizPair:
    def __init__(self, material, quiz):
        self.material = material
        self.quiz = quiz


class VideoQuizPair:
    def __init__(self, material, quiz):
        self.material = material
        self.quiz = quiz


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     app.setStyleSheet(Path("../styles.qss").read_text())
#     ex = QuizApp()
#     ex.show()
#     sys.exit(app.exec_())
