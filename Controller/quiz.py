import os
import sys
import yaml
from pathlib import Path
import random

from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWebEngineWidgets
from PyQt5.QtCore import QTimer


video_directory = os.path.join(os.path.dirname(__file__), "..", "View")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")
import video as video
import emotional_analysis as emotional_analysis

class InstructionsWidget(QWidget):
    def __init__(self, instruction_form, parent=None):
        super().__init__(parent)
        self.screen_layout = QVBoxLayout()
        self.instruction_form = instruction_form
        self.initUI()

    def initUI(self):
        self.form_content_widget = QScrollArea()
        self.form_content_widget.setWidgetResizable(True)
         # Create a label for "Pre Survey" heading
        self.instruction_form_heading = QLabel("Instructions")
        self.instruction_form_heading.setObjectName("heading1")
        self.instruction_form_heading.setFixedHeight(75)
        self.screen_layout.addWidget(self.instruction_form_heading)

        # Show reading text content
        self.form_content_label = QLabel(" ".join(self.instruction_form.get("text")))
        self.form_content_label.setWordWrap(True)
        self.form_content_widget.setWidget(self.form_content_label)

        self.screen_layout.addWidget(self.form_content_widget)

        # # Add reading material widget to screen layout
        self.setLayout(self.screen_layout)


class ConsentFormWidget(QWidget):
    def __init__(self, consent_form, parent=None):
        super().__init__(parent)
        self.screen_layout = QVBoxLayout()
        self.consent_form = consent_form
        self.initUI()
    
    def initUI(self):

        self.form_content_widget = QScrollArea()
        self.form_content_widget.setWidgetResizable(True)
         # Create a label for "Pre Survey" heading
        self.consent_form_heading = QLabel("Consent Form")
        self.consent_form_heading.setObjectName("heading1")
        self.consent_form_heading.setFixedHeight(75)
        self.screen_layout.addWidget(self.consent_form_heading)

        # Show reading text content
        self.form_content_label = QLabel(" ".join(self.consent_form.get("text")))
        self.form_content_label.setWordWrap(True)
        self.form_content_widget.setWidget(self.form_content_label)

        self.screen_layout.addWidget(self.form_content_widget)

        # # Add reading material widget to screen layout
        self.setLayout(self.screen_layout)


class PreSurveyWidget(QWidget):
    def __init__(self, pre_survey, submit_button, submit_quiz_button, parent=None):
        super().__init__(parent)
        self.pre_survey = pre_survey
        self.screen_layout = QVBoxLayout()
        # self.emotional_analysis = emotional_analysis

        # radio button
        self.buttonGroups = []  # for radio button groups
        self.question_grid_layout = QGridLayout()
        self.radio_group = QButtonGroup(self)
        self.next_button = submit_button
        self.submit_quiz_button = submit_quiz_button

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

    def update_submit_button(self):
        # self.show_recording_message("Recording will begin on next page")

        all_radio_buttons_selected = all(radio_group.checkedId() != -1 for radio_group in self.buttonGroups)

        # Check if all text fields are filled
        information_answers = [info_input.text() for info_input in self.findChildren(QLineEdit)]
        all_text_questions_answered = all(text_answer.strip() for text_answer in information_answers)
        
        self.next_button.setEnabled(all_radio_buttons_selected and all_text_questions_answered)
        if (all_radio_buttons_selected and all_text_questions_answered):
            self.submit_quiz_button.setEnabled(False)
        
    def get_answers(self): 
        
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
        

class IndividualInterestSurveyWidget(QWidget):
    def __init__(self, individual_interest_survey, next_button, submit_quiz_button, parent=None):
        super().__init__(parent)
        self.individual_interest_survey = individual_interest_survey
        self.screen_layout = QVBoxLayout()
        self.emotional_analysis = emotional_analysis
        # radio button
        self.buttonGroups = []  # for radio button groups
        self.question_grid_layout = QGridLayout()
        self.radio_group = QButtonGroup(self)
        self.next_button = next_button
        self.submit_quiz_button = submit_quiz_button

        self.recording_message = None
        self.flash_timer = QTimer(self)
        self.flash_state = False
        self.flash_count = 0
        self.max_flash_count = 2  # Set the maximum number of flashes

        self.initUI()


    def initUI(self):
        # Create a label for "Individual Interest survey" heading
        individual_interest_survey_heading = QLabel("Individual Interest Survey")
        individual_interest_survey_heading.setObjectName("heading1")
        individual_interest_survey_heading.setFixedHeight(75)
        self.screen_layout.addWidget(individual_interest_survey_heading)

        # Create a grid layout for scale ratings
        scale_rating_grid_layout = QGridLayout()
        option_list = [
            "Very true for me",
            "True for me",
            "Neuatral",
            "Not true for me",
            "Not true at all",
        ]

        for i, option in enumerate(option_list):
            option_label = QLabel(option)
            option_label.setObjectName("headGridWidget")
            scale_rating_grid_layout.addWidget(option_label, 0, i)
        
        # Add scale ratings to head grid layout
        head_grid_layout = QGridLayout()
        head_grid_layout.setColumnStretch(0, 1)
        head_grid_layout.setColumnStretch(1, 2)
        head_grid_layout.addItem(scale_rating_grid_layout, 1, 1)
        head_grid_widget = QWidget()
        head_grid_widget.setObjectName("headGridWidget")
        head_grid_widget.setLayout(head_grid_layout)
        head_grid_widget.setFixedHeight(75)
        self.screen_layout.addWidget(head_grid_widget)

        # Show Likert Scale questions
        for question_i, question in enumerate(self.individual_interest_survey.get("questions")):
            self.show_scale_questions(question_i, question)

        # Fix column stretch
        self.question_grid_layout.setColumnStretch(0, 1)
        self.question_grid_layout.setColumnStretch(1, 2)

        # Set layouts
        self.screen_layout.addItem(self.question_grid_layout)
        self.setLayout(self.screen_layout)
    
    def show_scale_questions(self, question_i, question):
        # Create a QLabel for question text and set it to word wrap
        question_label = QLabel(question.get("text"))
        question_label.setWordWrap(True)
        self.question_grid_layout.addWidget(question_label, question_i, 0)

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

    def show_recording_message(self, message):
        # Display a message saying "Recording will begin on next page"
        self.recording_message = QLabel(message)
        self.recording_message.setObjectName("recording_message")
        self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        self.screen_layout.addWidget(self.recording_message)

        # Start the flash timer to make the message flash
        self.flash_timer.timeout.connect(self.toggle_flash)
        self.flash_timer.start(500)  # Adjust the flash interval (in milliseconds) based on your preference

    def toggle_flash(self):
        # Toggle the flash state and update the message visibility accordingly
        self.flash_state = not self.flash_state
        self.recording_message.setVisible(self.flash_state)

        # Check if the maximum number of flashes is reached
        if self.flash_state and self.flash_count >= self.max_flash_count:
            self.flash_timer.stop()
            self.hide_recording_message()

        # Increment the flash count if the message is visible
        if self.flash_state:
            self.flash_count += 1

    def hide_recording_message(self):
        # Remove the recording message widget
         if self.recording_message:
            self.screen_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None

    def update_submit_button(self):
    
        all_radio_buttons_selected = all(radio_group.checkedId() != -1 for radio_group in self.buttonGroups)
        if (all_radio_buttons_selected):
            self.show_recording_message("Recording will begin on next page")
            self.submit_quiz_button.setEnabled(False)
            
        self.next_button.setEnabled(all_radio_buttons_selected)

    def get_answers(self):

        # Get the selected radio button options for scale questions
        selected_options = []
        for radio_group in self.buttonGroups:
            selected_option = radio_group.checkedId()
            if selected_option != -1:
                selected_options.append(selected_option)
        
        responses = selected_options
        # Save responses to a file
        with open(file_path, "a") as file:
            file.write("Individual Interest Survey Responses:\n")
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

        # show "Recording will begin now" message
        self.recording_message = None
        self.flash_timer = QTimer(self)
        self.flash_state = False
        self.flash_count = 0
        self.max_flash_count = 2  # Set the maximum number of flashes


        # initialize a timer to be displayed on screen
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        # create a timer label
        self.timer_label = QLabel("00:00:00", self)
        # align the timer to the top right corner
        self.timer_label.setAlignment(Qt.AlignRight)
        self.timer_label.setStyleSheet("font-size: 36px;")

        self.initUI()

    def initUI(self):
        try:
            self.setLayout(self.screen_layout)
            self.go_to_next_material()

        except Exception as e:
            print("An error occurred in initUI:", str(e))

    def show_recording_message(self, message):
        # Display a message saying "Recording will begin on next page"
        self.recording_message = QLabel(message)
        self.recording_message.setObjectName("recording_message")
        self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
        self.screen_layout.addWidget(self.recording_message)

        # Start the flash timer to make the message flash
        self.flash_timer.timeout.connect(self.toggle_flash)
        self.flash_timer.start(500)  # Adjust the flash interval (in milliseconds) based on your preference
    
    def toggle_flash(self):
        # Toggle the flash state and update the message visibility accordingly
        self.flash_state = not self.flash_state
        if self.recording_message:
            self.recording_message.setVisible(self.flash_state)

        # Check if the maximum number of flashes is reached
        if self.flash_state and self.flash_count >= self.max_flash_count:
            self.flash_timer.stop()
            self.hide_recording_message()

        # Increment the flash count if the message is visible
        if self.flash_state:
            self.flash_count += 1

    def hide_recording_message(self):
        # Remove the recording message widget
        if self.recording_message:
            self.screen_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None
    
    def update_timer(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.setText(time_str)

    def go_to_next_material(self):
        # set the timer layout
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

        # if timer hasn't already been started, start it
        if not self.timer.isActive():
            self.screen_layout.addWidget(self.timer_label)
            self.timer.start(1000) # update every second

        self.webview = None
        
        # Set start quiz button
        self.start_quiz_button = QPushButton("Start Quiz")
        self.screen_layout.addWidget(self.start_quiz_button)
        self.start_quiz_button.clicked.connect(self.go_to_next_question)

    def show_video(self):
        try:
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
            if self.reading_topic != "":
                self.reading_topic.setObjectName("heading2")
                self.screen_layout.addWidget(self.reading_topic)
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.video_url))
            self.screen_layout.addWidget(self.webview)

            if not self.timer.isActive():
                self.screen_layout.addWidget(self.timer_label)
                self.timer.start(1000) # update every second
            # Set start quiz button
            self.start_quiz_button = QPushButton("Start Quiz")
            self.screen_layout.addWidget(self.start_quiz_button)
            self.start_quiz_button.clicked.connect(self.go_to_next_question)

        except Exception as e:
            print("An error occurred in video func:", str(e))

    def go_to_next_question(self):
        try:
            if self.start_quiz_button:
                self.hide_recording_message()
                self.emotional_analysis.stop() # stop recording subject and performing emotional analysis
                print("stopping emotional analysis")
                # Delete reading text widgets
                if self.reading_text_widget:
                    self.reading_text_widget.deleteLater()
                    self.screen_layout.removeWidget(self.reading_text_heading)
                    self.reading_text_heading.deleteLater()
                    self.screen_layout.removeWidget(self.reading_topic)
                    self.reading_topic.deleteLater()

                if self.webview:
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
                self.show_recording_message("Recording will begin now")
                self.screen_layout.removeWidget(self.post_quiz_widget)
                self.post_quiz_widget.deleteLater()
                self.screen_layout.removeWidget(self.post_quiz_heading)
                self.post_quiz_heading.deleteLater()
                self.go_to_next_material()
                self.emotional_analysis.start()
                print("starting emotional analysis")
                return
        except Exception as e:
            print("An error occurred in go to next question:", str(e))

    def show_question(self):
        
        try:
            
            if self.question.get("name") == "post_quiz":
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

                # Create a grid layout for questions
                self.question_grid_layout = QGridLayout()

                # Fix the column stretch
                self.question_grid_layout.setColumnStretch(0, 1)
                self.question_grid_layout.setColumnStretch(1, 2)

                # Show Likert Scale questions
                
                self.show_scale_questions(0, self.question)
            
            elif self.question.get("name") == "situational_interest":
                heading_label = QLabel(
                    "Answer the following with very true for me/true for me/neutral/not true for me/not true at all"  
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
                    "Very true for me",
                    "True for me",
                    "Neutral",
                    "Not true for me",
                    "Not true at all",
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

                # Create a grid layout for questions
                self.question_grid_layout = QGridLayout()

                # Fix the column stretch
                self.question_grid_layout.setColumnStretch(0, 1)
                self.question_grid_layout.setColumnStretch(1, 2)

                # Show Likert Scale questions
                self.show_scale_questions(1, self.question)
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
            print("An error occurred in show_question:", str(e))

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
    
        self.question_grid_widget = QWidget()

        self.question_grid_layout = QGridLayout()

        
        
        if self.question.get("hasSubtext"):
            
            if self.question.get("name") == "post_quiz":

                for sub_question_i, subtext in enumerate(question.get("postQuizSubtext")):
                        # Create label for subtext
                    question_label = QLabel(subtext)
                    question_label.setWordWrap(True)

                    # Add label to the question grid layout
                    self.question_grid_layout.addWidget(
                        question_label, sub_question_i + 0, 0
                    )
                    self.question_grid_widget.setLayout(self.question_grid_layout)
                    self.post_quiz_layout.addWidget(self.question_grid_widget)

                    # Show options
                    self.show_scale_options(sub_question_i + question_i, question)

            else:
                for sub_question_i, subtext in enumerate(question.get("situationalInterestSubtext")):
                        # Create label for subtext
                    question_label = QLabel(subtext)
                    question_label.setWordWrap(True)

                    # Add label to the question grid layout
                    self.question_grid_layout.addWidget(
                        question_label, sub_question_i + 1, 0
                    )
                    self.question_grid_widget.setLayout(self.question_grid_layout)
                    self.post_quiz_layout.addWidget(self.question_grid_widget)

                    # Show options
                    self.show_scale_options(sub_question_i + question_i, question)
        else:
            self.show_scale_options(question_i, self.question)
    

    def show_scale_options(self, question_i, question):
        # Define the scale options
        if(question.get("name") == "post_quiz"):
            option_list = [
                "strongly agree",
                "agree",
                "neither",
                "disagree",
                "strongly disagree",
            ]
        else:
            option_list = [
                    "Very true for me",
                    "True for me",
                    "Neutral",
                    "Not true for me",
                    "Not true at all",
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
        # stop timer
        self.timer.stop()
        elapsed_time = self.elapsed_time
          # Convert elapsed time to a human-readable format
        hours = elapsed_time // 3600
        minutes = (elapsed_time % 3600) // 60
        seconds = elapsed_time % 60
        # Write the formatted elapsed time to the file
        with open(file_path, "a") as file:
            file.write("Total time taken: {:02d} hours, {:02d} minutes, {:02d} seconds\n".format(hours, minutes, seconds))


        self.hide_recording_message()
        print("stopping emotional analysis")
        print("Emotions detected throughout session: " ,self.emotional_analysis.detected_emotions)


        for i in reversed(range(self.post_quiz_layout.count())):
            self.post_quiz_layout.itemAt(i).widget().deleteLater()

        self.completed_label = QLabel("Thank you for completing the survey! We appreciate your time")
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
        self.instructions_widget = InstructionsWidget(instructions)


        # create an instance of ConsentFormWidget
        self.consent_form_widget = ConsentFormWidget(consent_form)

        # next buttons

        self.go_to_individual_interest_survey_button = QPushButton("Next")
        self.go_to_individual_interest_survey_button.setEnabled(False)

        self.go_to_postquiz_button = QPushButton("Next")
        self.go_to_postquiz_button.setEnabled(False)

        # submit survey responses buttons
        self.submit_presurvey_button = QPushButton("Submit Quiz")
        self.submit_individual_interest_survey_button = QPushButton("Submit Quiz")

        # create the 3 widgets
        self.pre_survey_widget = PreSurveyWidget(pre_survey, self.go_to_individual_interest_survey_button, self.submit_presurvey_button)
        self.post_quiz_widget = PostQuizWidget(self.display_content, self.emotional_analysis)
        self.individual_interest_survey_widget = IndividualInterestSurveyWidget(individual_interest_survey, self.go_to_postquiz_button, self.submit_individual_interest_survey_button)

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

        # Add a submit quiz button
        self.screen_layout.addWidget(self.submit_presurvey_button)
        self.submit_presurvey_button.clicked.connect(self.pre_survey_widget.update_submit_button)

        
        # add next button
        self.screen_layout.addWidget(self.go_to_individual_interest_survey_button)
        self.go_to_individual_interest_survey_button.clicked.connect(self.transition_to_individual_interest_survey)

    def transition_to_individual_interest_survey(self):

        responses = self.pre_survey_widget.get_answers()
        # remove pre-survey widgets
        self.screen_layout.removeWidget(self.pre_survey_widget)
        self.pre_survey_widget.deleteLater()

        # remove submit quiz button
        self.screen_layout.removeWidget(self.submit_presurvey_button)
        self.submit_presurvey_button.deleteLater()

        # remove next button
        self.screen_layout.removeWidget(self.go_to_individual_interest_survey_button)
        self.go_to_individual_interest_survey_button.deleteLater()

        self.screen_layout.addWidget(self.individual_interest_survey_widget)
        # show post_quiz
        self.individual_interest_survey_widget.show()

        # Add a submit quiz button
        self.screen_layout.addWidget(self.submit_individual_interest_survey_button)
        self.submit_individual_interest_survey_button.clicked.connect(self.individual_interest_survey_widget.update_submit_button)

        # add next button
        self.screen_layout.addWidget(self.go_to_postquiz_button)
        self.go_to_postquiz_button.clicked.connect(self.transition_to_post_quiz)

    def transition_to_post_quiz(self):

        self.individual_interest_survey_widget.get_answers()
        # remove pre-survey widgets
        self.screen_layout.removeWidget(self.individual_interest_survey_widget)
        self.individual_interest_survey_widget.deleteLater()

        # remove submit quiz button
        self.screen_layout.removeWidget(self.submit_individual_interest_survey_button)
        self.submit_individual_interest_survey_button.deleteLater()

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

        # Initialize an empty list to store MaterialQuizPair instances
        self.text_pairs = []
        self.video_pairs = []

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
                    with open(text_quiz_path, "r", encoding="utf-8") as quiz_file:
                        text_quiz_data = yaml.load(quiz_file, Loader=yaml.FullLoader)
                    with open(video_quiz_path, "r", encoding="utf-8") as quiz_file:
                        video_quiz_data = yaml.load(quiz_file, Loader=yaml.FullLoader)

                    # Create a TextQuizPair instance and append to the list

                    self.text_pair = TextQuizPair(material_data, text_quiz_data)
                    self.text_pairs.append(self.text_pair)
                  

                    # Create a VideoQuizPair instance and append to the list
                    self.video_pair = VideoQuizPair(material_data, video_quiz_data)
                    self.video_pairs.append(self.video_pair)
                else:
                    print("something's wrong")

        # randomly pick a text from text_pairs
        self.rand_text = random.choice(self.text_pairs)

        # print the index of self.rand_text
        index = self.text_pairs.index(self.rand_text)

        # remove the element at index from video_pairs
    
        
        self.video_pairs.remove(self.video_pairs[index]) # remove the picked text from the list so that it's corresponding video cannot be picked
        
        # pick video from other topic
        self.rand_video = self.video_pairs[0]
        
        # generate a random number to determine sequence of video and text (if rand num == 1, text first; else video first)
        rand_num = random.randint(1, 2)
        
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