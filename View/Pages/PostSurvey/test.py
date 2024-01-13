import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QTextBrowser, QPushButton
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtCore import Qt

class ReadingWidget(QWidget):
    def __init__(self, texts):
        super().__init__()
        self.initUI(texts)

    def initUI(self, texts):
        self.texts = texts
        self.page_index = 0

        # 创建 QTextBrowser 对象
        self.text_browser = QTextBrowser()
        self.text_browser.setOpenExternalLinks(True)  # 允许打开外部链接

        # 创建按钮
        self.next_page_button = QPushButton("Next Page")
        self.next_page_button.clicked.connect(self.show_next_page)

        self.prev_page_button = QPushButton("Previous Page")
        self.prev_page_button.clicked.connect(self.show_prev_page)

        # 初始化界面
        self.show_current_page()

        # 创建布局
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_browser)
        layout.addWidget(self.prev_page_button)
        layout.addWidget(self.next_page_button)

    def show_current_page(self):
        # 根据当前页码生成文本
        start_index = self.page_index
        end_index = start_index + 1
        current_page_text = self.texts[start_index:end_index]

        # 使用 QTextDocument 控制分页
        document = QTextDocument()
        cursor = QTextCursor(document)

        for text in current_page_text:
            cursor.insertHtml(text)

        self.text_browser.setDocument(document)

    def show_next_page(self):
        # 显示下一页
        if self.page_index < len(self.texts) - 1:
            self.page_index += 1
            self.show_current_page()

    def show_prev_page(self):
        # 显示上一页
        if self.page_index > 0:
            self.page_index -= 1
            self.show_current_page()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    sample_texts = [
        "<p>This mission placed humans on the moon for the very first time, contributing to a better understanding of Earth's only natural satellite.</p>",
        "<p>The solar system has no shortage of moons...</p>",
        # 添加更多段落...
    ]

    widget = ReadingWidget(sample_texts)
    widget.show()

    sys.exit(app.exec_())
