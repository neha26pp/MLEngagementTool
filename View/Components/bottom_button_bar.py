import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QApplication, QLabel, QVBoxLayout

BOTTOM_BUTTON_H = 80  # bottom button bar height
BOTTOM_BUTTON_W = 200  # bottom button bar width


class BottomButtonBar(QWidget):
    def __init__(self):
        super().__init__()

        self.back_func = None
        self.cancel_func = None
        self.next_func = None
        self.back_label = QLabel("")
        self.back_label.setFixedSize(BOTTOM_BUTTON_W, BOTTOM_BUTTON_H)
        self.back_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.next_label = QLabel("")
        self.next_label.setFixedSize(BOTTOM_BUTTON_W, BOTTOM_BUTTON_H)
        self.next_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.back_button = QPushButton("Back")
        self.back_button.setObjectName("bottomButton")
        self.back_button.setFixedSize(BOTTOM_BUTTON_W, BOTTOM_BUTTON_H)

        self.cancel_button = QPushButton("Cancel Session")
        self.cancel_button.setObjectName("bottomButton")
        self.cancel_button.setFixedSize(BOTTOM_BUTTON_W, BOTTOM_BUTTON_H)

        self.next_button = QPushButton("Next")
        self.next_button.setObjectName("bottomButton")
        self.next_button.setFixedSize(BOTTOM_BUTTON_W, BOTTOM_BUTTON_H)

        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.back_button)
        self.main_layout.addWidget(self.back_label)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.cancel_button)
        self.main_layout.addStretch(1)
        self.main_layout.addWidget(self.next_label)
        self.main_layout.addWidget(self.next_button)
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(14, 0, 14, 0)

        self.hide()

    def connect_signals(self, back_func, cancel_func, next_func):
        self.back_func = back_func
        self.cancel_func = cancel_func
        self.next_func = next_func

        if back_func is None:
            self.back_button.setEnabled(False)
        else:
            self.back_button.clicked.connect(back_func)

        self.cancel_button.clicked.connect(cancel_func)
        self.next_button.clicked.connect(next_func)

    def set_button_info(self, back_label, next_label):
        self.back_label.setText(back_label)
        self.next_label.setText(next_label)

    def disconnect_signals(self):
        if self.back_func is not None:
            self.back_button.disconnect()
        if self.cancel_button is not None:
            self.cancel_button.disconnect()
        if self.next_button is not None:
            self.next_button.disconnect()

    def show_buttons(self):
        self.show()

    def hide_buttons(self):
        self.hide()

    def set_next_button_enabled(self, is_enable):
        self.next_button.setEnabled(is_enable)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(Path("../../styles.qss").read_text())
    screen = BottomButtonBar()
    screen.show()

    sys.exit(app.exec_())
