import os
import unittest

from PyQt5.QtWidgets import QApplication

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../View"))
os.chdir(project_root)

from View.post_survey_widget import PostQuizWidget


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
        # self.app.exit()
        pass

    def test_show_recording_message(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        self.assertIsNotNone(post_quiz_widget.recording_message)
        self.assertEqual(post_quiz_widget.recording_message.text(), "Recording will begin now")

    def test_hide_recording_message(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        post_quiz_widget.hide_recording_message()
        self.assertIsNone(post_quiz_widget.recording_message)

    def test_toggle_flash(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.show_recording_message("Recording will begin now")
        initial_flash_state = post_quiz_widget.flash_state
        post_quiz_widget.toggle_flash()
        self.assertNotEqual(post_quiz_widget.flash_state, initial_flash_state)

    def test_update_timer(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.timer.timeout.emit()
        self.assertEqual(post_quiz_widget.elapsed_time, 1)  # Assuming timer updates elapsed time

    def test_go_to_next_material(self):
        text = {"reading-text": {"topic": "Test", "text": ["Hello World!"]}}
        display_content = [TextQuizPair(text)]
        post_quiz_widget = PostQuizWidget(display_content, None, None, None)
        post_quiz_widget.go_to_next_material()
        self.assertEqual(post_quiz_widget.current_material, 1)

    def test_show_reading_material(self):
        text = {"reading-text": {"topic": "Test", "text": ["Hello World!"]}}
        display_content = [TextQuizPair(text)]
        post_quiz_widget = PostQuizWidget(display_content, None, None, None)
        post_quiz_widget.reading_text = {"topic": "Test", "text": ["Hello World!", ""]}
        post_quiz_widget.show_reading_material()

        self.assertIsNotNone(post_quiz_widget.reading_text_widget)
        self.assertIsNotNone(post_quiz_widget.reading_text_heading)
        self.assertIsNotNone(post_quiz_widget.start_quiz_button)

    def test_show_video(self):
        video = {"reading-text": {"video": "test_video_url"}}
        display_content = [VideoQuizPair(video)]
        post_quiz_widget = PostQuizWidget(display_content, None, None, None)
        post_quiz_widget.display_content = []
        post_quiz_widget.show_video()
        post_quiz_widget.reading_text = {"material": {"reading-text": {"video": "test_video_url"}}}
        self.assertIsNotNone(post_quiz_widget.reading_text_widget)
        self.assertIsNotNone(post_quiz_widget.reading_text_heading)
        self.assertIsNotNone(post_quiz_widget.start_quiz_button)

    def test_go_to_quiz(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.go_to_quiz()
        self.assertIsNone(post_quiz_widget.webview)
        self.assertIsNotNone(post_quiz_widget.next_button)

    def test_show_completed_message(self):
        post_quiz_widget = PostQuizWidget(None, None, None, None)
        post_quiz_widget.show_completed_message()
        self.assertIsNotNone(post_quiz_widget.completed_label)


if __name__ == '__main__':
    unittest.main()
