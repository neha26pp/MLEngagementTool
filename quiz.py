#encoding: utf8
import sys
import codecs
import yaml
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, \
    QLineEdit, QHBoxLayout, QFormLayout, QCheckBox, QGridLayout
class PreSurveyWidget(QWidget):
    def __init__(self, quiz_data, parent=None):
        super().__init__(parent)
        self.quiz_data = quiz_data
        self.screen_layout = QVBoxLayout()
        # radio button
        self.buttonGroups = [] # for radio button groups
        self.question_grid_layout = QGridLayout()
        self.radio_group = QButtonGroup(self)

        self.initUI()

    def initUI(self):
        # Split the data
        pre_survey = self.quiz_data[0]
        pre_survey_information = pre_survey["Pre-survey"][0].get("information")
        pre_survey_question = pre_survey["Pre-survey"][1].get("questions")

        pre_survey_heading = QLabel("Pre Survey")
        pre_survey_heading.setObjectName("heading1")
        pre_survey_heading.setFixedHeight(70)
        self.screen_layout.addWidget(pre_survey_heading)

        # Display personal information form
        info_grid_layout = QGridLayout()
        for i, info in enumerate(pre_survey_information):
            info_form_layout = QFormLayout()
            info_label = QLabel(info)
            info_input = QLineEdit()
            if i%3 < 2 :
                info_label.setFixedWidth(120)
            else:
                info_label.setFixedWidth(250)
            info_input.setFixedWidth(125)
            info_form_layout.addRow(info_label, info_input)
            info_grid_layout.addItem(info_form_layout, int(i/3), i%3)
        # set column stretch
        info_grid_layout.setColumnStretch(0, 1)
        info_grid_layout.setColumnStretch(1, 1)
        info_grid_layout.setColumnStretch(2, 2)
        # set fixed height
        info_grid_widget = QWidget()
        info_grid_widget.setLayout(info_grid_layout)
        info_grid_widget.setFixedHeight(100)

        # add the form to the screen
        self.screen_layout.addWidget(info_grid_widget)

        # Display personal information question table
        # display the head of personal information questions
        head_grid_layout = QGridLayout()
        head_grid_layout.setColumnStretch(0, 1)
        head_grid_layout.setColumnStretch(1, 2)
        head_question_label = QLabel("Questions")
        head_question_label.setObjectName("headGridWidget")
        head_grid_layout.addWidget(head_question_label, 0, 0)
        head_question_label = QLabel("Scale Ratings")
        head_question_label.setObjectName("headGridWidget")
        head_grid_layout.addWidget(head_question_label, 0, 1)

        scale_rating_grid_layout = QGridLayout()
        option_list = ["strongly agree", "agree", "neither", "disagree", "strongly disagree"]

        for i, option in enumerate(option_list):
            option_label = QLabel(option)
            option_label.setObjectName("headGridWidget")
            scale_rating_grid_layout.addWidget(option_label, 0, i)
        head_grid_layout.addItem(scale_rating_grid_layout, 1, 1)
        # self.screen_layout.addItem(head_grid_layout)
        head_grid_widget = QWidget()
        head_grid_widget.setObjectName("headGridWidget")
        head_grid_widget.setLayout(head_grid_layout)
        head_grid_widget.setFixedHeight(70)
        self.screen_layout.addWidget(head_grid_widget)
        # show Likert Scale questions
        for question_i, question in enumerate(pre_survey_question):
            self.show_scale_questions(question_i, question)
        # fix the column stretch
        self.question_grid_layout.setColumnStretch(0, 1)
        self.question_grid_layout.setColumnStretch(1, 2)
        self.screen_layout.addItem(self.question_grid_layout)

        self.setLayout(self.screen_layout)

    def show_scale_questions(self, question_i, question):
        question_label = QLabel(question.get("text"))
        question_label.setWordWrap(True)
        self.question_grid_layout.addWidget(question_label, question_i, 0)

        if question.get("type") == "scale":
            if question.get("hasSubtext"):
                for sub_question_i, text in enumerate(question.get("subtext")):
                    question_label = QLabel(text)
                    question_label.setWordWrap(True)
                    self.question_grid_layout.addWidget(question_label, question_i + sub_question_i + 1, 0)
                    # Show options
                    self.show_scale_options(question_i + sub_question_i + 1)
            else:
                # Show options
                self.show_scale_options(question_i)

    def show_scale_options(self, question_i):
        option_list = ["strongly agree", "agree", "neither", "disagree", "strongly disagree"]
        radio_group = QButtonGroup(self)
        layout_scale_option = QGridLayout()

        for radio_button_i, _ in enumerate(option_list):
            radio_button = QRadioButton()
            radio_group.addButton(radio_button, radio_button_i)
            layout_scale_option.addWidget(radio_button, 0, radio_button_i)

        self.question_grid_layout.addLayout(layout_scale_option, question_i, 1)
        self.buttonGroups.append(radio_group)

    def get_answers(self):
        information_answers = [info_input.text() for info_input in self.information_widgets]
        selected_option = self.radio_group.checkedId()
        return information_answers + [selected_option]

class PostQuizWidget(QWidget):
    def __init__(self, quiz_data, parent=None):
        super().__init__(parent)
        # read data
        self.quiz_data = quiz_data
        self.post_quiz = self.quiz_data[1]
        self.post_quiz_parts = self.post_quiz["Post-quiz"]

        self.question_grid_layout = QGridLayout()
        self.screen_layout = QVBoxLayout()

        self.current_question = 0
        self.current_heading = 0
        self.initUI()

    def initUI(self):
        try:
            self.setLayout(self.screen_layout)
            # show reading material text
            self.show_reading_material()
        except Exception as e:
            print("An error occurred:", str(e))

    def show_reading_material(self):
        # initialize reading text widget
        self.reading_text_widget = QWidget()
        self.reading_text_layout = QVBoxLayout()
        self.reading_text_widget.setLayout(self.reading_text_layout)
        # self.reading_text_widget.setStyleSheet("background: lightblue") # debugging

        # set reading text heading
        self.reading_text_heading = QLabel("Reading Text")
        self.reading_text_heading.setObjectName("heading1")
        self.reading_text_heading.setFixedHeight(70)
        self.screen_layout.addWidget(self.reading_text_heading)
        # show reading text content
        self.reading_text = QLabel(self.post_quiz_parts[0]['readingText'])
        self.reading_text.setWordWrap(True)
        self.reading_text_layout.addWidget(self.reading_text)
        # set start quiz button
        self.start_quiz_button = QPushButton('Start Quiz')
        self.reading_text_layout.addWidget(self.start_quiz_button)
        self.start_quiz_button.clicked.connect(self.go_to_next_question)
        self.screen_layout.addWidget(self.reading_text_widget)

    def show_video(self):
        pass

    def go_to_next_question(self):
        try:
            if self.start_quiz_button:
                # delete reading text widgets
                self.reading_text_layout.removeWidget(self.reading_text_widget)
                self.reading_text_widget.deleteLater()
                self.reading_text_layout.deleteLater()
                self.screen_layout.removeWidget(self.reading_text_heading)
                self.reading_text_heading.deleteLater()
                self.start_quiz_button = None
                # add post quiz heading
                post_quiz_heading = QLabel("Post Quiz")
                post_quiz_heading.setObjectName("heading1")
                post_quiz_heading.setFixedHeight(70)
                self.screen_layout.addWidget(post_quiz_heading)
            else:
                # remove post quiz widgets
                self.screen_layout.removeWidget(self.post_quiz_widget)
                self.post_quiz_widget.deleteLater()

            # initialize post quiz widget
            # this widget is for all post quiz widget excluding heading 1 and next button
            self.post_quiz_widget = QWidget()
            self.post_quiz_layout = QVBoxLayout()
            self.post_quiz_widget.setLayout(self.post_quiz_layout)
            self.screen_layout.addWidget(self.post_quiz_widget)
            self.post_quiz_widget.setStyleSheet("background: lightblue")  # debugging

            headings = self.post_quiz_parts[1]['quiz']

            if self.current_heading < len(headings):
                current_part = headings[self.current_heading]
                # show heading text
                heading = current_part.get('heading')
                if heading != '':
                    heading_label = QLabel(heading)
                    self.post_quiz_layout.addWidget(heading_label)
                # get questions data
                self.current_part_questions = current_part.get("questions")
                if self.current_question < len(self.current_part_questions):
                    # show the current question
                    self.question = self.current_part_questions[self.current_question]
                    self.show_question()
                    # update question index
                    self.current_question += 1
                else:
                    # update heading index
                    self.current_question = 0
                    self.current_heading += 1
                # set next button
                self.submit_button = QPushButton('Next')
                self.post_quiz_layout.addWidget(self.submit_button)
                self.submit_button.clicked.connect(self.go_to_next_question)
        except Exception as e:
            print("An error occurred:", str(e))

    def show_question(self):
            try:
                self.buttonGroups = [] # for radio buttons
                if self.question.get("type") == "scale":
                    # Display personal information question table
                    # display the head of personal information questions
                    head_grid_layout = QGridLayout()
                    head_grid_layout.setColumnStretch(0, 1)
                    head_grid_layout.setColumnStretch(1, 2)
                    head_question_label = QLabel("Questions")
                    head_question_label.setObjectName("headGridWidget")
                    head_grid_layout.addWidget(head_question_label, 0, 0)
                    head_question_label = QLabel("Scale Ratings")
                    head_question_label.setObjectName("headGridWidget")
                    head_grid_layout.addWidget(head_question_label, 0, 1)
                    # display scale ratings
                    scale_rating_grid_layout = QGridLayout()
                    option_list = ["strongly agree", "agree", "neither", "disagree", "strongly disagree"]
                    for i, option in enumerate(option_list):
                        option_label = QLabel(option)
                        option_label.setObjectName("headGridWidget")
                        scale_rating_grid_layout.addWidget(option_label, 0, i)
                    head_grid_layout.addItem(scale_rating_grid_layout, 1, 1)
                    head_grid_widget = QWidget()
                    head_grid_widget.setObjectName("headGridWidget")
                    head_grid_widget.setLayout(head_grid_layout)
                    head_grid_widget.setFixedHeight(70)
                    self.post_quiz_layout.addWidget(head_grid_widget)
                    # show Likert Scale questions
                    for question_i, question in enumerate(self.current_part_questions):
                        self.show_scale_questions(question_i, question)
                    # fix the column stretch
                    self.question_grid_layout.setColumnStretch(0, 1)
                    self.question_grid_layout.setColumnStretch(1, 2)
                    self.post_quiz_layout.addItem(self.question_grid_layout)

                if self.question.get("text") != '':
                    # show question text
                    question_label = QLabel(self.question.get("text"))
                    self.post_quiz_layout.addWidget(question_label)

                if self.question.get('type') == 'single':
                    self.show_single_choice_options() # show single choice options
                if self.question['type'] == 'multiple':
                    self.show_multiple_choice_options() # show multiple choice options
            except Exception as e:
                print("An error occurred:", str(e))
    def show_single_choice_options(self):
        try:
            radio_group = QButtonGroup()
            for i, option in enumerate(self.question.get('options')):
                radio_button = QRadioButton(option)
                self.post_quiz_layout.addWidget(radio_button)
                radio_group.addButton(radio_button, i)
        except Exception as e:
            print("An error occurred:", str(e))

    def show_multiple_choice_options(self):
        for i, option in enumerate(self.question.get('options')):
            checkbox = QCheckBox(option)
            self.post_quiz_layout.addWidget(checkbox)

    def show_scale_questions(self, question_i, question):
        question_label = QLabel(question.get("text"))
        if question_label != '':
            question_label.setWordWrap(True)
            self.question_grid_layout.addWidget(question_label, question_i, 0)
            question_i += 1
        if question.get("hasSubtext"):
            for sub_question_i, subtext in enumerate(question.get("subtext")):
                question_label = QLabel(subtext)
                question_label.setWordWrap(True)
                self.question_grid_layout.addWidget(question_label, question_i + sub_question_i, 0)
                self.post_quiz_layout.addLayout(self.question_grid_layout)
                # Show options
                self.show_scale_options(question_i + sub_question_i)
            else:
                # Show options
                self.show_scale_options(question_i)
    def show_scale_options(self, question_i):
        option_list = ["strongly agree", "agree", "neither", "disagree", "strongly disagree"]
        radio_group = QButtonGroup(self)
        layout_scale_option = QGridLayout()

        for radio_button_i, _ in enumerate(option_list):
            radio_button = QRadioButton()
            radio_group.addButton(radio_button, radio_button_i)
            layout_scale_option.addWidget(radio_button, 0, radio_button_i)

        self.question_grid_layout.addLayout(layout_scale_option, question_i, 1)
        self.buttonGroups.append(radio_group)

    def show_completed_message(self):
        for i in reversed(range(self.post_quiz_layout.count())):
            self.post_quiz_layout.itemAt(i).widget().deleteLater()

        self.completed_label = QLabel('Post Quiz Completed!')
        self.screen_layout.addWidget(self.completed_label)

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz Application')
        self.setGeometry(100, 100, 1200, 300)

        # Read quiz data from YAML
        with open('quiz.yaml', 'r', encoding="utf-8") as yaml_file:
            quiz_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # pass data to pre survey and post quiz
        self.pre_survey_widget = PreSurveyWidget(quiz_data)
        self.post_quiz_widget = PostQuizWidget(quiz_data)

        # show pre-survey
        self.screen_layout = QVBoxLayout()
        self.screen_layout.addWidget(self.pre_survey_widget)
        self.setLayout(self.screen_layout)
        # add next button
        self.submit_button = QPushButton('Next')
        self.screen_layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.transition_to_post_quiz)

    def transition_to_post_quiz(self):
        # remove pre-survey widgets
        self.screen_layout.removeWidget(self.pre_survey_widget)
        self.pre_survey_widget.deleteLater()
        # remove next button
        self.screen_layout.removeWidget(self.submit_button)
        self.submit_button.deleteLater()
        # add post-quiz widgets
        self.screen_layout.addWidget(self.post_quiz_widget)
        # show post-quiz
        self.post_quiz_widget.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('styles.qss').read_text())
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
