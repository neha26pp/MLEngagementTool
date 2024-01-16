from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtWidgets import QLabel


class Timer:
    time_updated = pyqtSignal(str)

    def __init__(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.elapsed_time = 0
        self.timer_label = QLabel("00:00:00", self)
        # create a timer label

        self.timer_label.setFixedHeight(36)
        # align the timer to the top right corner
        self.timer_label.setAlignment(Qt.AlignRight)
        self.timer_label.setStyleSheet("font-size: 36px;")

    def start_timer(self):
        self.timer.start(1000)  # update every second

    def stop_timer(self):
        self.timer.stop()

    def update_timer(self):
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.setText(time_str)
        self.time_updated.emit(time_str)

    def reset_timer(self):
        self.elapsed_time = 0
        self.timer_label.setText("00:00:00")

    def get_timer_label(self):
        return self.timer_label.text()

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
