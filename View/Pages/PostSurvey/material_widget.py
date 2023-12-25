from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget


class MaterialWidget(QWidget):
    def __init__(self, material_type, material_content):
        super().__init__()
        self.material_type = material_type
        self.material_content = material_content
        self.screen_layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        if self.material_type == "text":
            self.show_reading_text()
        else:
            self.show_watch_video_button()

        self.setLayout(self.screen_layout)

    def show_reading_text(self):
        print(self.material_content)

        # Initialize reading text widget
        self.material_widget = QScrollArea(self)
        self.material_widget.setWidgetResizable(True)
        # Set reading text heading
        self.material_heading = HeaderWidget("Reading Text")
        self.reading_topic = QLabel(self.material_content.get("topic"))

        # Show reading topic if available-start
        if self.reading_topic != "":
            self.reading_topic.setObjectName("heading2")
            self.material_widget.setWidget(self.reading_topic)

        # Show reading text content
        self.material_label = QLabel(" ".join(self.material_content.get("text")))
        self.material_label.setWordWrap(True)
        self.material_widget.setWidget(self.material_label)

        # Set layout
        self.screen_layout.addWidget(self.material_heading)
        self.screen_layout.addWidget(self.material_widget)

    def show_watch_video_button(self):
        self.post_survey_heading = HeaderWidget("Post Survey")
        self.video_button = QPushButton("Watch Video")
        self.video_button.clicked.connect(self.show_video)

        self.screen_layout.addWidget(self.post_survey_heading)
        self.screen_layout.addStretch(1)
        self.screen_layout.addWidget(self.video_button, 1)
        self.screen_layout.addStretch(1)

    def show_video(self):
        try:
            # Reset layout
            while self.screen_layout.count():
                item = self.screen_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()
                else:
                    del item

            # Set reading text heading
            self.material_heading = HeaderWidget("Video")

            # Set video url
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.material_content))

            # Set layout
            self.screen_layout.addWidget(self.material_heading)
            self.screen_layout.addWidget(self.webview, 1)
        except Exception as e:
            print("An error occurred in show_video func in MaterialWidget:", str(e))

