from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget


class QuizWidget(QWidget):
    def __init__(self, post_quiz):
        super().__init__()
        self.post_quiz = post_quiz
        self.screen_layout = QVBoxLayout()

        self.initUI()

    def initUI(self):
        try:
            # Set post quiz heading
            self.post_quiz_heading = HeaderWidget("Post Quiz")

            # create a new webview to display the quiz
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.post_quiz))

            self.screen_layout.addWidget(self.post_quiz_heading)
            self.screen_layout.addWidget(self.webview, 1)
            self.setLayout(self.screen_layout)
        except Exception as e:
            print("An error occurred in QuizWidget widget:", str(e))
