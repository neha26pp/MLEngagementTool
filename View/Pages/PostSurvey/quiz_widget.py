from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget
from View.Pages.page import Page


class QuizWidget(Page):
    def __init__(self, post_quiz):
        super().__init__(heading_text="Post Quiz")
        self.post_quiz = post_quiz

        try:
            # create a new webview to display the quiz
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.post_quiz))
            self.main_layout.addWidget(self.webview, 1)
        except Exception as e:
            print("An error occurred in QuizWidget widget:", str(e))
