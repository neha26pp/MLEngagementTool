from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget


class MaterialWidget(QWidget):
    watch_video_button_signal = pyqtSignal()
    reading_material_finished_signal = pyqtSignal()
    reading_material_not_finished_signal = pyqtSignal()

    def __init__(self, material_type, material_content):
        super().__init__()
        self.material_type = material_type
        self.material_content = material_content
        self.screen_layout = QVBoxLayout()
        self.page_index = 0

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
        self.text_browser = QTextBrowser()

        # Set reading text heading
        self.material_heading = HeaderWidget("Reading Text")
        self.reading_topic = QLabel(self.material_content.get("topic"))

        # Show reading text content
        self.show_current_reading_text_page()

        # Create page buttons
        self.next_page_button = QPushButton("Next Page")
        self.next_page_button.setObjectName("bottomButton")
        self.next_page_button.clicked.connect(self.show_next_page)
        self.next_page_button.setMinimumHeight(50)
        self.next_page_button.setMaximumHeight(50)
        if len(self.material_content.get("text")) <= 1:
            self.next_page_button.setEnabled(False)

        self.prev_page_button = QPushButton("Previous Page")
        self.prev_page_button.setObjectName("bottomButton")
        self.prev_page_button.clicked.connect(self.show_prev_page)
        self.prev_page_button.setMinimumHeight(50)
        self.prev_page_button.setMaximumHeight(50)
        self.prev_page_button.setEnabled(False)

        page_button_layout = QHBoxLayout()
        page_button_layout.addWidget(self.prev_page_button)
        page_button_layout.addWidget(self.next_page_button)

        # Set layout
        self.screen_layout.addWidget(self.material_heading)
        self.screen_layout.addWidget(self.text_browser)
        self.screen_layout.addLayout(page_button_layout)

    def show_current_reading_text_page(self):
        start_index = self.page_index
        end_index = start_index + 1
        current_page_text = self.material_content.get("text")[start_index:end_index]

        # Wrap the text in a <div> with padding
        wrapped_text = '<div style="margin: 80px;">' + ' '.join(current_page_text) + '</div>'

        document = QTextDocument()
        document.setHtml(wrapped_text)

        self.text_browser.setDocument(document)
        self.text_browser.setStyleSheet("font-size: 24px")

    def show_next_page(self):
        if self.page_index < len(self.material_content.get("text")) - 1:
            self.page_index += 1
            self.show_current_reading_text_page()
            self.prev_page_button.setEnabled(True)
        if self.page_index == len(self.material_content.get("text")) - 1:
            self.next_page_button.setEnabled(False)
            self.reading_material_finished_signal.emit()

    def show_prev_page(self):
        if self.page_index > 0:
            self.page_index -= 1
            self.show_current_reading_text_page()
            self.next_page_button.setEnabled(True)
            self.reading_material_not_finished_signal.emit()
        if self.page_index <= 1:
            self.prev_page_button.setEnabled(False)

    def show_watch_video_button(self):
        self.post_survey_heading = HeaderWidget("Post Survey")
        self.video_button = QPushButton("Watch Video")
        self.video_button.clicked.connect(self.show_video)
        self.video_button.clicked.connect(self.watch_video_button_signal.emit)

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

