import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QTimer

from header_widget import HeaderWidget

from data_router import TextQuizPair

file_path = os.path.join(os.path.dirname(__file__), "..", "quiz_data", "responses.txt")


class PostQuizWidget(QWidget):
    def __init__(self, display_content, emotional_analysis, stimulus1_type, stimulus2_type, parent=None):
        super().__init__(parent)
        # read data
        self.post_quiz_heading = None
        self.emotional_analysis = emotional_analysis
        self.display_content = display_content

        # initialize layouts
        self.screen_layout = QVBoxLayout()

        # initialize index
        self.current_question = 0
        self.current_material = 0

        # show "Recording will begin now" message
        self.recording_message = None
        self.flash_timer = QTimer(self)
        self.flash_state = False
        self.flash_count = 0
        self.max_flash_count = 2  # Set the maximum number of flashes

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        self.webview = None
        self.next_button = QPushButton("Next")
        self.initUI()

    def initUI(self):
        try:
            self.setLayout(self.screen_layout)
            self.go_to_next_material()

        except Exception as e:
            print("An error occurred in initUI:", str(e))

    def show_recording_message(self, message):
        try:
            # Display a message saying "Recording will begin on next page"
            self.recording_message = QLabel(message)
            self.recording_message.setObjectName("recording_message")
            self.recording_message.setStyleSheet("font-size: 20px; font-weight: bold; color: red;")
            self.screen_layout.addWidget(self.recording_message)

            # Start the flash timer to make the message flash
            self.flash_timer.timeout.connect(self.toggle_flash)
            self.flash_timer.start(500)  # Adjust the flash interval (in milliseconds) based on your preference
        except Exception as e:
            print("An error occurred in show_recording_message func:", str(e))

    def hide_recording_message(self):
        # Remove the recording message widget
        if self.recording_message:
            self.screen_layout.removeWidget(self.recording_message)
            self.recording_message.deleteLater()
            self.recording_message = None

    def go_to_next_material(self):
        if self.post_quiz_heading:
            self.post_quiz_heading.deleteLater()
            self.screen_layout.removeWidget(self.post_quiz_heading)
            self.post_quiz_heading = None

        if self.next_button:
            self.next_button.deleteLater()
            self.screen_layout.removeWidget(self.next_button)
            self.next_button = None

        if self.webview:
            self.screen_layout.removeWidget(self.webview)
            self.webview.deleteLater()
            self.webview = None

        if self.current_material < len(self.display_content):
            # display content has either [video, text] or [text, video]
            if self.display_content[self.current_material].text is True:
                self.reading_text = self.display_content[self.current_material].material.get("reading-text")
                self.text = self.reading_text.get("text")
                self.post_quiz = self.reading_text.get("text_quiz")
                self.show_reading_material()
            else:
                self.video_button = QPushButton("Watch Video")
                self.screen_layout.addWidget(self.video_button)
                self.video_button.clicked.connect(self.show_video)
                self.reading_text = self.display_content[self.current_material].material.get("reading-text")
                self.video_url = self.reading_text.get("video")
                self.post_quiz = self.reading_text.get("video_quiz")
            self.current_material += 1

        else:
            self.show_completed_message()

    def show_reading_material(self):
        if self.webview:
            self.screen_layout.removeWidget(self.webview)
            self.webview.deleteLater()
            self.webview = None

        # Initialize reading text widget
        self.reading_text_widget = QScrollArea()
        # self.reading_text_widget.setStyleSheet("background: lightblue") # Debugging
        self.reading_text_widget.setWidgetResizable(True)
        # Set reading text heading
        self.reading_text_heading = HeaderWidget("Reading Text")
        self.screen_layout.addWidget(self.reading_text_heading)

        self.reading_topic = QLabel(self.reading_text.get("topic"))

        # Show reading topic if available
        if self.reading_topic != "":
            self.reading_topic.setObjectName("heading2")
            self.reading_text_widget.setWidget(self.reading_topic)

        # Show reading text content
        self.reading_text_label = QLabel(" ".join(self.reading_text.get("text")))
        self.reading_text_label.setWordWrap(True)
        self.reading_text_widget.setWidget(self.reading_text_label)

        # Add reading material widget to screen layout
        self.screen_layout.addWidget(self.reading_text_widget)

        self.start_quiz_button = QPushButton("Start Quiz")
        self.screen_layout.addWidget(self.start_quiz_button)
        self.start_quiz_button.clicked.connect(self.go_to_quiz)

    def show_video(self):
        try:
            # Get video URL
            if self.video_button:
                self.video_button.deleteLater()
                self.screen_layout.removeWidget(self.video_button)

            if self.webview:
                self.screen_layout.removeWidget(self.webview)
                self.webview.deleteLater()

            self.reading_text_widget = QScrollArea()
            self.reading_text_widget.setWidgetResizable(True)
            # Set reading text heading
            self.reading_text_heading = HeaderWidget("Video")
            self.screen_layout.addWidget(self.reading_text_heading)

            self.reading_topic = QLabel(self.reading_text.get("topic"))

            # Show video topic if available
            if self.reading_topic != "":
                self.reading_topic.setObjectName("heading2")
                self.reading_text_widget.setWidget(self.reading_topic)
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.video_url))
            self.reading_text_widget.setWidget(self.webview)
            self.screen_layout.addWidget(self.reading_text_widget)

            # Set start quiz button
            self.start_quiz_button = QPushButton("Start Quiz")
            self.screen_layout.addWidget(self.start_quiz_button)
            self.start_quiz_button.clicked.connect(self.go_to_quiz)

        except Exception as e:
            print("An error occurred in video func:", str(e))

    def go_to_quiz(self):
        try:
            # remove reading text widget
            self.screen_layout.removeWidget(self.reading_text_widget)
            self.reading_text_widget.deleteLater()

            self.screen_layout.removeWidget(self.reading_text_heading)
            self.reading_text_heading.deleteLater()

            # remove start quiz button
            self.screen_layout.removeWidget(self.start_quiz_button)
            self.start_quiz_button.deleteLater()

            # remove the previous webview widget
            if self.webview:
                self.screen_layout.removeWidget(self.webview)
                self.webview.deleteLater()

            # Set post quiz heading
            self.post_quiz_heading = HeaderWidget("Post Quiz")
            self.screen_layout.addWidget(self.post_quiz_heading)

            # create a new webview to display the quiz
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.post_quiz))
            self.screen_layout.addWidget(self.webview)

            # create a "Next" button
            self.next_button = QPushButton("Next")
            self.screen_layout.addWidget(self.next_button)
            self.next_button.clicked.connect(self.go_to_next_material)
        except Exception as e:
            print("An error occurred in go_to_quiz func:", str(e))

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
            file.write(
                "Total time taken: {:02d} hours, {:02d} minutes, {:02d} seconds\n".format(hours, minutes, seconds))

        self.hide_recording_message()
        print("stopping emotional analysis")
        print("Emotions detected throughout session: ", self.emotional_analysis.detected_emotions)

        header = HeaderWidget("Finish")
        self.screen_layout.addWidget(header)

        self.completed_layout = QVBoxLayout()
        self.completed_layout.setAlignment(Qt.AlignCenter)
        self.completed_layout.addStretch(1)

        self.completed_label = QLabel("Thank You!\n Your responses have been recorded.")
        self.completed_label.setFixedHeight(400)
        self.completed_label.setObjectName("completeMessage")
        self.completed_label.setAlignment(Qt.AlignCenter)
        self.completed_layout.addWidget(self.completed_label)

        # self.view_report_button = QPushButton("View Report")
        # self.view_report_button.setFixedSize(850, 150)

        # self.view_report_button.setObjectName("viewReportButton")
        # self.completed_layout.addWidget(self.view_report_button, alignment=Qt.AlignCenter)
        # self.completed_layout.addStretch(1)

        self.screen_layout.addLayout(self.completed_layout)


