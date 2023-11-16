from PyQt5.QtWidgets import *
from header_widget import HeaderWidget

class InstructionsWidget(QWidget):
    def __init__(self, instruction_form, parent=None):
        super().__init__(parent)
        self.form_content_label = None
        self.instruction_form_heading = None
        self.form_content_widget = None
        self.screen_layout = QVBoxLayout()
        self.instruction_form = instruction_form
        self.initUI()

    def initUI(self):
        self.form_content_widget = QScrollArea(parent=None)
        self.form_content_widget.setWidgetResizable(True)
        # Create a label for "Instructions" heading
        self.instruction_form_heading = HeaderWidget("Instructions")
        self.screen_layout.addWidget(self.instruction_form_heading)

        # Show reading text content
        self.form_content_label = QLabel(" ".join(self.instruction_form.get("text")))
        self.form_content_label.setWordWrap(True)
        self.form_content_widget.setWidget(self.form_content_label)

        self.screen_layout.addWidget(self.form_content_widget)

        # # Add reading material widget to screen layout
        self.setLayout(self.screen_layout)
