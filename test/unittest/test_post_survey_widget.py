import os
import unittest
from unittest.mock import MagicMock

from PyQt5.QtWidgets import QApplication

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../View"))
os.chdir(project_root)

from View.Pages.PostSurvey.post_survey_widget import PostQuizWidget


class TextQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = True


class VideoQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = False


class TestPostQuizWidget(unittest.TestCase):
    def setUp(self):
        self.app = QApplication([])

    def tearDown(self):
        self.app.exit()

    def test_show_recording_message(self):
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        self.assertIsNotNone(post_quiz_widget.recording_message)
        self.assertEqual(post_quiz_widget.recording_message.text(), "Recording will begin now")

    def test_hide_recording_message(self):
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        post_quiz_widget.hide_recording_message()
        self.assertIsNone(post_quiz_widget.recording_message)

    def test_toggle_flash(self):
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        initial_flash_state = post_quiz_widget.flash_state
        post_quiz_widget.toggle_flash()
        self.assertNotEqual(post_quiz_widget.flash_state, initial_flash_state)

    def test_update_timer(self):
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.timer.timeout.emit()
        self.assertEqual(post_quiz_widget.elapsed_time, 1)  # Assuming timer updates elapsed time

    def test_go_to_next_material(self):
        # it should increase the material index by 1
        post_quiz_widget = PostQuizWidget(None)
        self.assertEqual(post_quiz_widget.current_material, 0)
        post_quiz_widget.go_to_next_material()
        self.assertEqual(post_quiz_widget.current_material, 1)

    def test_show_reading_material(self):
        # it should set reading text widget
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.reading_text = {"topic": "Test", "text": ["Hello World!", ""]}
        post_quiz_widget.show_reading_material()

        self.assertIsNotNone(post_quiz_widget.reading_text_widget )

    def test_show_video(self):
        # it should set video widget
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.display_content = []
        post_quiz_widget.show_video()
        post_quiz_widget.reading_text = {"material": {"reading-text": {"video": "test_video_url"}}}
        self.assertIsNotNone(post_quiz_widget.video_widget)

    def test_go_to_quiz(self):
        # it should set quiz widget
        post_quiz_widget = PostQuizWidget(None)
        post_quiz_widget.go_to_quiz()
        self.assertIsNotNone(post_quiz_widget.quiz_widget)


if __name__ == '__main__':
    unittest.main()
