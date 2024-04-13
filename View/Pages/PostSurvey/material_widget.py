from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtGui import QTextDocument
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import *

from View.Components.header_widget import HeaderWidget
from View.Pages.page import Page


class MaterialWidget(Page):
    watch_video_button_signal = pyqtSignal()
    reading_material_finished_signal = pyqtSignal()
    reading_material_not_finished_signal = pyqtSignal()

    def __init__(self, material_type, material_content, topic):
        super().__init__(heading_text="do not show")
        self.material_type = material_type
        self.material_content = material_content
        # self.main_layout = QVBoxLayout()
        self.page_index = 0

      
        if self.material_type == "text":
            
            self.show_reading_text()
        else:
            
            self.show_video()

        # self.setLayout(self.main_layout)

    def show_reading_text(self):
        print("IN SHOW READING TEXT: ------")
        print(self.material_content)

        # Initialize reading text widget
        self.text_browser = QTextBrowser(parent=None)

     

        # Show reading text content
        self.show_current_reading_text_page()

        # Set layout
        
        self.main_layout.addWidget(self.text_browser)

        # Set page button
        if len(self.material_content.get("text")) > 1:
            # Create page buttons
            self.next_page_button = QPushButton("Next Page")
            self.next_page_button.setObjectName("bottomButton")
            self.next_page_button.clicked.connect(self.show_next_page)
            self.next_page_button.setMinimumHeight(50)
            self.next_page_button.setMaximumHeight(50)

            self.prev_page_button = QPushButton("Previous Page")
            self.prev_page_button.setObjectName("bottomButton")
            self.prev_page_button.clicked.connect(self.show_prev_page)
            self.prev_page_button.setMinimumHeight(50)
            self.prev_page_button.setMaximumHeight(50)
            self.prev_page_button.setEnabled(False)

            page_button_layout = QHBoxLayout()
            page_button_layout.addWidget(self.prev_page_button)
            page_button_layout.addWidget(self.next_page_button)

            self.main_layout.addLayout(page_button_layout)

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
        if self.page_index < 1:
            self.prev_page_button.setEnabled(False)

    def show_video(self):
        try:
            # Set video heading
            # self.header = HeaderWidget("Video")

            # Set video url
            self.webview = QWebEngineView()
            self.webview.setUrl(QUrl(self.material_content))

            # Set layout
            # self.main_layout.addWidget(self.header)
            self.main_layout.addWidget(self.webview, 1)

        except Exception as e:
            print("An error occurred in show_video func in MaterialWidget:", str(e))

