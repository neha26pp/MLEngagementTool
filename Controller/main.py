import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import os
from pathlib import Path
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QRadioButton, QButtonGroup, \
    QLineEdit, QFormLayout, QCheckBox, QGridLayout, QScrollArea
import quiz

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(Path('../styles.qss').read_text())
    root = quiz.QuizApp()
    root.show()
    sys.exit(app.exec_())

    main()