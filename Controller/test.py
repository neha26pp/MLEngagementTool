import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QStackedWidget, QHBoxLayout


class ReadingWidget(QWidget):
    def __init__(self, texts):
        super().__init__()
        self.initUI(texts)

    def initUI(self, texts):
        self.stacked_widget = QStackedWidget()

        for text in texts:
            page_widget = QWidget()
            layout = QVBoxLayout(page_widget)
            label = QLabel(text)
            layout.addWidget(label, alignment=Qt.AlignCenter)

            self.stacked_widget.addWidget(page_widget)

        # 添加上一页和下一页按钮
        prev_button = QPushButton("Previous")
        next_button = QPushButton("Next")

        prev_button.clicked.connect(self.show_previous_page)
        next_button.clicked.connect(self.show_next_page)

        button_layout = QHBoxLayout()
        button_layout.addWidget(prev_button)
        button_layout.addWidget(next_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addLayout(button_layout)

    def show_previous_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index > 0:
            self.stacked_widget.setCurrentIndex(current_index - 1)

    def show_next_page(self):
        current_index = self.stacked_widget.currentIndex()
        if current_index < self.stacked_widget.count() - 1:
            self.stacked_widget.setCurrentIndex(current_index + 1)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    sample_texts = ["Page 1: This is the content of page 1.",
                    "Page 2: This is the content of page 2.",
                    "Page 3: This is the content of page 3."]

    widget = ReadingWidget(sample_texts)
    widget.show()

    sys.exit(app.exec_())
