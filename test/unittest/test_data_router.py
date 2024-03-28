import os
import unittest
from unittest.mock import MagicMock

from PyQt5.QtWidgets import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
os.chdir(project_root)

from Controller.data_router import QuizApp

class TestQuizApp(unittest.TestCase):
    def setUp(self):
        # create a Quiz App instance
        self.app = QApplication([])
        self.quiz_app = QuizApp()
        self.quiz_app.main_stack_widget = MagicMock()
        self.quiz_app.bottom_button_bar_widget = MagicMock()

    def tearDown(self):
        # clean up after each test case run
        self.app.exit()

    def test_switch_to_branch_show_bottom_button_bar(self):
        # it should show the bottom button bar when on the branch
        self.quiz_app.switch_to_branch(1)
        self.quiz_app.bottom_button_bar_widget.show.assert_called()
        self.quiz_app.switch_to_branch(2)
        self.quiz_app.bottom_button_bar_widget.show.assert_called()

    def test_switch_to_branch_hide_bottom_button_bar(self):
        # it should hide the bottom button bar when on the dashboard screen
        self.quiz_app.switch_to_branch(0)
        self.quiz_app.bottom_button_bar_widget.hide.assert_called()

    def test_switch_to_branch_enable_next_button(self):
        # it should set next bottom enabled
        self.quiz_app.switch_to_branch(0)
        self.quiz_app.bottom_button_bar_widget.set_next_button_enabled.assert_called_once_with(True)

    def test_switch_to_branch_disable_next_button(self):
        # it should disable the next button on the branch Data Analyze
        self.quiz_app.switch_to_branch(2)
        self.quiz_app.bottom_button_bar_widget.set_next_button_enabled.assert_called_once_with(False)


if __name__ == '__main__':
    unittest.main()
