from PyQt5.QtWidgets import *
from View.Pages.page import Page


class InstructionsWidget(Page):
    def __init__(self, instruction_form, heading_text="Instructions"):
        super().__init__(heading_text=heading_text)
        self.instruction_form = instruction_form
        self.form_content_widget = QScrollArea(parent=None)
        self.form_content_widget.setWidgetResizable(True)

        # Show instruction form
        self.form_content_label = QLabel(" ".join(self.instruction_form.get("text")))
        self.form_content_label.setWordWrap(True)
        self.form_content_widget.setWidget(self.form_content_label)

        # Set layout
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(self.form_content_widget)
