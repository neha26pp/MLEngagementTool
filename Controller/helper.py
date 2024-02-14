import sys
import yaml
from PyQt5.QtWidgets import QMessageBox


def read_yaml(file_path):
    with open(file_path, "r", encoding="utf-8") as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.FullLoader)


def show_confirmation():
    # create message box
    reply = QMessageBox.question(QMessageBox(), 'Confirmation', 'Are you sure you want to exit?',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    # process confirmation
    if reply == QMessageBox.Yes:
        sys.exit()  # if yes, exit the system
    else:
        pass  # if no, cancel exit