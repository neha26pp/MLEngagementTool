import os
import sys
from pathlib import Path
import random
from PyQt5.Qt import *

from Controller import eye_tracker
from Controller.data_router import read_yaml
from Controller.data_router import show_confirmation
from View.Pages.PostSurvey.finish_widget import FinishWidget
from View.Pages.PostSurvey.material_widget import MaterialWidget
from View.Pages.PostSurvey.quiz_widget import QuizWidget
from View.Components.bottom_button_bar import BottomButtonBar

video_directory = os.path.join(os.path.dirname(__file__), "../..")
sys.path.append(video_directory)
file_path = os.path.join(os.path.dirname(__file__), "../..", "quiz_data", "responses.txt")


class PostQuizWidget(QWidget):
    def __init__(self, emotional_analysis):
        super().__init__()
        # read data
        self.reading_text_widget = None
        self.post_quiz_heading = None
        # self.eye_tracker = None
        self.eye_tracker = eye_tracker.EyeTracker()

        self.emotional_analysis = emotional_analysis
        self.display_content = None

        # initialize layouts
        self.screen_layout = QVBoxLayout()
        self.screen_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout = QVBoxLayout()
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout()

        # initialize index
        self.current_question = 0
        self.current_material = 0

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
        self.timer_label.setFixedHeight(36)
        # align the timer to the top right corner
        self.timer_label.setAlignment(Qt.AlignRight)
        self.timer_label.setStyleSheet("font-size: 36px; margin-right: 4px")

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        self.webview = None

        self.bottom_button_widget = BottomButtonBar()
        self.finish_widget = FinishWidget()

        self.initUI()

    def initUI(self):
        try:
            self.loadMaterialQuizPairs()

            # Set up layout
            self.container_layout.addWidget(self.content_widget)
            self.screen_layout.addLayout(self.container_layout)
            self.screen_layout.addWidget(self.timer_label)
            self.screen_layout.addWidget(self.bottom_button_widget)
            self.bottom_button_widget.show()
            self.setLayout(self.screen_layout)

            self.go_to_next_material()

        except Exception as e:
            print("An error occurred in initUI:", str(e))

    def loadMaterialQuizPairs(self):
        try:
            # Directory where subdirectories containing material and quiz files are located
            directory = "../quiz_data/post_quiz"  # Update to your directory path

            # Initialize an empty list to store texts and videos
            self.texts = []
            self.videos = []

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
                    if os.path.exists(material_path) and os.path.exists(text_quiz_path) and os.path.exists(
                            video_quiz_path):
                        # Read the contents of material and text quiz and video quiz files
                        material_data = read_yaml(material_path)

                        # get the text and video material
                        self.text_pairs = TextQuizPair(material_data)
                        self.texts.append(self.text_pairs)

                        # Create a VideoQuizPair instance and append to the list
                        self.video_pairs = VideoQuizPair(material_data)
                        self.videos.append(self.video_pairs)

            # randomly pick a text
            self.rand_text = random.choice(self.texts)
            index = self.texts.index(self.rand_text)

            # remove the element at index from videos (to not pick the video belonging to same topic)
            self.videos.remove(self.videos[
                                   index])  # remove the picked text from the list so that it's corresponding video cannot be picked

            # pick video from other topic
            self.rand_video = self.videos[0]
            # generate a random number to determine sequence of video and text
            # (if rand num == 1, text first; else video first)
            rand_num = random.randint(1, 2)

            if rand_num == 1:
                self.display_content.append(self.rand_text)
                self.display_content.append(self.rand_video)
            else:
                self.display_content.append(self.rand_video)
                self.display_content.append(self.rand_text)
            print("display_content:", self.display_content)

        except Exception as e:
            print("error occurs in loadMaterialQuizPairs: ", e)

    def show_recording_message(self, message):
        try:
            # Display a message saying "Recording will begin on next page"
            self.recording_message = QLabel(message)
            self.recording_message.setObjectName("recording_message")
            self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
            self.content_layout.addWidget(self.recording_message)

            # Start the flash timer to make the message flash
            self.flash_timer.timeout.connect(self.toggle_flash)
            self.flash_timer.start(500)  # Adjust the flash interval (in milliseconds) based on your preference
        except Exception as e:
            print("An error occurred in show_recording_message func:", str(e))

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
            self.content_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None

    def update_timer(self):
        try:
            self.elapsed_time += 1
            hours = self.elapsed_time // 3600
            minutes = (self.elapsed_time % 3600) // 60
            seconds = self.elapsed_time % 60
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            self.timer_label.setText(time_str)

        except Exception as e:
            print("An error occurred in update_timer func:", str(e))

    def go_to_next_material(self):
        try:
            # Reset the container_layout
            self.reset_content_widget()

            if self.current_material < len(self.display_content):
                # display content has either [video, text] or [text, video]
                if self.display_content[self.current_material].text is True:
                    self.reading_text = self.display_content[self.current_material].material.get("reading-text")
                    self.text = self.reading_text.get("text")
                    self.post_quiz = self.reading_text.get("text_quiz")

                    self.show_reading_material()

                else:
                    self.reading_text = self.display_content[self.current_material].material.get("reading-text")
                    self.video_url = self.reading_text.get("video")
                    self.post_quiz = self.reading_text.get("video_quiz")
                    self.bottom_button_widget.set_next_button_enabled(False)

                    self.show_video()

                self.current_material += 1

            else:
                # go to finish screen
                self.bottom_button_widget.hide()
                self.show_completed_message()

        except Exception as e:
            print("An error occurred in go_to_next_material:", str(e))

    def show_reading_material(self):
        try:
            if self.emotional_analysis:
                print("starting emotional analysis before stimulus")
                self.emotional_analysis.start()

            if self.eye_tracker:
                print("starting eyetracking before stimulus")
                self.eye_tracker.start()

            # Reset the container_layout
            self.reset_content_widget()

            # create an instance of MaterialWidget
            self.reading_text_widget = MaterialWidget("text", self.reading_text)

            # Add reading material widget to screen layout
            self.content_layout.addWidget(self.reading_text_widget)

            # if timer hasn't already been started, start it
            if not self.timer.isActive():
                self.timer.start(1000)  # update every second

            # Set bottom button bar
            self.bottom_button_widget.disconnect_signals()
            self.bottom_button_widget.connect_signals(None, show_confirmation, self.go_to_quiz)
            self.bottom_button_widget.set_button_info(None, "Start Quiz")
            if len(self.reading_text.get("text")) > 1:
                self.bottom_button_widget.set_next_button_enabled(False)
            self.reading_text_widget.reading_material_finished_signal.connect(
                lambda: self.bottom_button_widget.set_next_button_enabled(True))
            self.reading_text_widget.reading_material_not_finished_signal.connect(
                lambda: self.bottom_button_widget.set_next_button_enabled(False))

        except Exception as e:
            print("An error occurred in show_reading_material:", str(e))

    def show_video(self):
        try:
            if self.emotional_analysis:
                print("starting emotional analysis before stimulus")
                self.emotional_analysis.start()

            if self.eye_tracker:
                print("starting eyetracking before stimulus")
                self.eye_tracker.start()

            # Reset the container_layout
            self.reset_content_widget()

            # create an instance of MaterialWidget
            self.video_widget = MaterialWidget("video", self.video_url)
            self.content_layout.addWidget(self.video_widget)

            if not self.timer.isActive():
                self.timer.start(1000)  # update every second

            # Set bottom button bar
            self.bottom_button_widget.disconnect_signals()
            self.bottom_button_widget.connect_signals(None, show_confirmation, self.go_to_quiz)
            self.bottom_button_widget.set_button_info(None, "Start Quiz")
            self.bottom_button_widget.set_next_button_enabled(True)

        except Exception as e:
            print("An error occurred in video func:", str(e))

    def go_to_quiz(self):
        try:
            print("go to quiz")

            if self.emotional_analysis:
                print("stopping emotional analysis after stimulus")
                self.emotional_analysis.stop()

            if self.eye_tracker:
                thread_activity = self.emotional_analysis.get_activity()
                print("stopping eyetracking after stimulus")
                self.eye_tracker.stop()

            # Reset the container_layout
            self.reset_content_widget()

            # create an instance of QuizWidget
            self.quiz_widget = QuizWidget(post_quiz=self.post_quiz)
            self.content_layout.addWidget(self.quiz_widget, 1)

            # Set bottom button bar
            self.bottom_button_widget.disconnect_signals()
            self.bottom_button_widget.connect_signals(None, show_confirmation, self.go_to_next_material)

            if self.current_material < len(self.display_content):
                self.bottom_button_widget.set_button_info(None, "Next Material")
            else:
                self.bottom_button_widget.set_button_info(None, "Finish")

        except Exception as e:
            print("An error occurred in go_to_quiz func:", str(e))

    def show_completed_message(self):
        try:
            # stop recording subject and performing emotional analysis
            if self.emotional_analysis:
                print("stopping emotional analysis")
                self.emotional_analysis.stop()
                print("Emotions detected throughout session: ", self.emotional_analysis.detected_emotions)

            if self.eye_tracker:
                print("stopping eyetracking")
                self.eye_tracker.stop()

            # stop timer
            self.timer.stop()

            # Calculate and format elapsed time
            elapsed_time = self.elapsed_time
            time_format = "{:02d}:{:02d}:{:02d}"
            formatted_time = time_format.format(elapsed_time // 3600, (elapsed_time % 3600) // 60, elapsed_time % 60)

            # Write the formatted elapsed time to the file
            with open(file_path, "a") as file:
                file.write("Total time taken: {}\n".format(formatted_time))

            # Hide recording message
            self.hide_recording_message()

            # Set the instance of FinishWidget
            self.content_layout.addWidget(self.finish_widget)

        except Exception as e:
            print("An error occurred in show_completed_message func:", str(e))

    def reset_content_widget(self):
        try:
            # remove content widget from  container layout
            self.container_layout.removeWidget(self.content_widget)
            self.content_widget.deleteLater()

            # create new content widget and layout
            self.content_widget = QWidget()
            self.content_layout = QVBoxLayout()
            self.content_layout.setContentsMargins(0, 0, 0, 0)

            # set up content widget and layout
            self.content_widget.setLayout(self.content_layout)
            self.container_layout.addWidget(self.content_widget)
        except Exception as e:
            print("An error occurred in reset_content_widget func:", str(e))


class TextQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = True


class VideoQuizPair:
    def __init__(self, material):
        self.material = material
        self.text = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("../../styles.qss").read_text())
    screen = PostQuizWidget()
    screen.show()
    sys.exit(app.exec_())
