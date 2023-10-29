import sys
import yaml
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, \
    QLineEdit

class QuizApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Quiz Application')
        self.setGeometry(200, 100, 1000, 300)

        # Read quiz data from YAML
        with open('quiz.yaml', 'r') as yaml_file:
            quiz_data = yaml.load(yaml_file, Loader=yaml.FullLoader)

        # Split quiz data
        self.pre_survey = quiz_data[0]
        self.post_quiz = quiz_data[1]

        self.pre_survey_information = self.pre_survey["Pre-survey"][0].get("information")
        self.pre_survey_question = self.pre_survey["Pre-survey"][1].get("questions")
        self.post_quiz_text = self.post_quiz["Post-quiz"][0].get("Text")
        self.post_quiz_question = self.post_quiz["Post-quiz"][1].get("questions")

        # Variables to track the current question and answers
        self.current_question = 0
        self.pre_survey_answers = []

        self.layout = QVBoxLayout()

        self.show_pre_survey()  # Call the method to display the pre-survey

        self.submit_button = QPushButton('Next')
        self.layout.addWidget(self.submit_button)
        self.submit_button.clicked.connect(self.transition_to_post_quiz)  # Connect to the next_question method

        self.setLayout(self.layout)

    def show_pre_survey(self):
        self.current_question = 0

        # Display personal information questions
        self.information_widgets = []
        for info in self.pre_survey_information:
            info_label = QLabel(info)
            info_input = QLineEdit()
            self.information_widgets.append(info_input)
            self.layout.addWidget(info_label)
            self.layout.addWidget(info_input)

        for question in self.pre_survey_question:
            question_label = QLabel(question.get("text"))
            self.layout.addWidget(question_label)

            radio_group = QButtonGroup()

            for i, option in enumerate(question.get("options")):
                radio_button = QRadioButton(option)
                self.layout.addWidget(radio_button)
                radio_group.addButton(radio_button, i)

        self.radio_group = radio_group

    def transition_to_post_quiz(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()
        self.show_post_quiz()


    def show_post_quiz(self):
        self.current_question = 0

        # Clear the existing widgets
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().deleteLater()

        if self.current_question < len(self.post_quiz_question):
            # Show the next post-quiz question
            self.question_label.setText(self.post_quiz_question[self.current_question]['text'])
            for i, option in enumerate(self.post_quiz_question[self.current_question]['options']):
                radio_button = QRadioButton(option)
                self.layout.addWidget(radio_button)
                self.radio_group.addButton(radio_button, i)
        else:
            # The quiz is completed
            self.show_result()

        self.submit_button.setText('Next')
        self.submit_button.clicked.disconnect()
        self.submit_button.clicked.connect(self.next_question)


    def next_question(self):
        if self.current_question < len(self.pre_survey_information):
            information_answers = [info_input.text() for info_input in self.information_widgets]
            self.pre_survey_answers.append(information_answers)
        else:
            selected_option = self.radio_group.checkedId()
            if self.current_question < len(self.pre_survey_information) + len(self.pre_survey_question):
                self.pre_survey_answers.append(selected_option)

        self.current_question += 1

        if self.current_question < len(self.pre_survey_information):
            # Display the next pre-survey question
            self.question_label.setText(self.pre_survey_question[self.current_question]['text'])
            for i, option in enumerate(self.pre_survey_question[self.current_question]['options']):
                self.radio_group.button(i).setText(option)
        elif self.current_question == len(self.pre_survey_information):
            # Show the post-quiz
            self.show_post_quiz()
        else:
            # The quiz is completed
            self.show_result()


    def show_result(self):
        self.question_label.setText('Quiz Completed!')
        # Process and display the answers here

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = QuizApp()
    ex.show()
    sys.exit(app.exec_())
