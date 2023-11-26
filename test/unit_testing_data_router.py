import os
import unittest

from PyQt5.QtWidgets import *

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../View"))
os.chdir(project_root)
from Controller.data_router import QuizApp


class TestQuizApp(unittest.TestCase):
    def setUp(self):
        # create a Quiz App instance
        self.app = QApplication([])
        self.quiz_app = QuizApp()

    def tearDown(self):
        # clean up after each test case run
        self.app.exit()

    def test_initUI(self):
        # check if widget variables are created
        self.assertIsNotNone(self.quiz_app.stacked_widget)
        self.assertIsInstance(self.quiz_app.screen_layout, QVBoxLayout)
        self.assertIsInstance(self.quiz_app.bottomButtonLayout, QHBoxLayout)
        self.assertIsInstance(self.quiz_app.bottomButtonWidget, QWidget)

    def test_back_button_clicked(self):
        self.assertNotEqual(self.quiz_app.stacked_widget.count(), 0)
        for index in range(self.quiz_app.stacked_widget.count()):
            # set the current screen index
            self.quiz_app.stacked_widget.setCurrentIndex(index)

            # click on Back button
            self.quiz_app.back_button_clicked()

            # check if going back to the previous screen
            expected_index = index - 1 if index > 0 else 0
            self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), expected_index)

    def test_next_button_clicked(self):
        self.assertNotEqual(self.quiz_app.stacked_widget.count(), 0)
        for index in range(self.quiz_app.stacked_widget.count()):
            # set the current screen index
            self.quiz_app.stacked_widget.setCurrentIndex(index)

            # click on Back button
            self.quiz_app.next_button_clicked()

            # check if going back to the next screen
            expected_index = index + 1 if index < self.quiz_app.stacked_widget.count() - 1 \
                else self.quiz_app.stacked_widget.count() - 1
            self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), expected_index)

    def test_update_start_pre_survey_button(self):
        self.quiz_app.agree_checkbox.setChecked(True)
        self.quiz_app.update_start_pre_survey_button()
        self.assertTrue(self.quiz_app.next_button.isEnabled())

        self.quiz_app.agree_checkbox.setChecked(False)
        self.quiz_app.update_start_pre_survey_button()
        self.assertFalse(self.quiz_app.next_button.isEnabled())

    def test_next_button_clicked_start_page(self):
        # set index as 0
        self.quiz_app.stacked_widget.setCurrentIndex(0)

        # click on Next Button
        self.quiz_app.next_button_clicked()

        # check if current index is 1
        self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), 1)

        # check if bottom button widget is available
        self.assertFalse(self.quiz_app.bottomButtonWidget.isVisible())

        # check heading
        found_label = self.quiz_app.instructions_widget.findChild(QLabel, "heading1")
        self.assertIsNotNone(found_label)
        self.assertEqual(found_label.text(), "Instructions")

    def test_next_button_clicked_consent_form(self):
        # set index as 1
        self.quiz_app.stacked_widget.setCurrentIndex(1)

        # click on Next Button
        self.quiz_app.next_button_clicked()

        # check if current index is 2
        self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), 2)

        # check if the agree checkbox is available and next_button is not enable
        self.assertFalse(self.quiz_app.agree_checkbox.isVisible())
        self.assertFalse(self.quiz_app.next_button.isEnabled())

        # check heading
        found_label = self.quiz_app.consent_form_widget.findChild(QLabel, "heading1")
        self.assertIsNotNone(found_label)
        self.assertEqual(found_label.text(), "Consent Form")

    def test_next_button_clicked_pre_survey(self):
        # set index as 2
        self.quiz_app.stacked_widget.setCurrentIndex(2)

        # click on Next Button
        self.quiz_app.next_button_clicked()

        # check if current index is 2
        self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), 3)

        # check if the agree checkbox is hidden and next_button is enable
        self.assertFalse(self.quiz_app.agree_checkbox.isVisible())
        self.assertTrue(self.quiz_app.next_button.isEnabled())

        # check heading
        found_label = self.quiz_app.pre_survey_widget.findChild(QLabel, "heading1")
        self.assertIsNotNone(found_label)
        self.assertEqual(found_label.text(), "Pre Survey")

    def test_next_button_clicked_post_survey(self):
        # set the index as the second last one
        self.quiz_app.stacked_widget.setCurrentIndex(self.quiz_app.stacked_widget.count() - 2)

        # click on Next Button
        self.quiz_app.next_button_clicked()

        # check if current index is the last one
        self.assertEqual(self.quiz_app.stacked_widget.currentIndex(), self.quiz_app.stacked_widget.count() - 1)

        # check heading
        found_button = self.quiz_app.post_quiz_widget.findChild(QPushButton)
        self.assertIsNotNone(found_button)
        self.assertEqual(found_button.text(), "Watch Video")


if __name__ == '__main__':
    unittest.main()
