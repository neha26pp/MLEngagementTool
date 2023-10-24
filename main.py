import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("My PyQt App")
    label = QLabel("Hello, PyQt!")
    window.setCentralWidget(label)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
