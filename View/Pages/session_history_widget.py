import sys
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from View.Components.header_widget import HeaderWidget


class SessionHistoryWidget(QWidget):
    select_model_signal = pyqtSignal(int, str)

    def __init__(self, session_history):
        super().__init__()
        self.student_data = session_history
        # create header
        header = HeaderWidget("Analyze Data")

        # create title label
        title_label = QLabel("Session History")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(200)
        title_label.setAlignment(Qt.AlignCenter)

        # Create table
        self.table = QTableWidget(self)
        self.table.setFixedWidth(1500)
        self.table.setMinimumHeight(500)
        self.table.setColumnCount(8)
        self.table_header_list = ["Student Name", "Date", "Stimulus 1", "Stimulus 2",
                                  "Score(SVR Eye)", "Score(SVR Emotion)", "Score(SVR Fusion)", ""]
        self.table.setHorizontalHeaderLabels(self.table_header_list)
        self.table.setContentsMargins(5, 5, 5, 5)
        self.table.setColumnWidth(len(self.table_header_list) - 1, 200)  # Set width for the last Column

        # Populate table with student data
        self.populate_table(session_history)

        table_layout = QHBoxLayout()
        table_layout.addStretch(1)
        table_layout.addWidget(self.table, stretch=4)
        table_layout.addStretch(1)

        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(header)
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)
        main_layout.addStretch(1)
        main_layout.addLayout(table_layout)
        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def populate_table(self, session_history):
        try:
            data_key_list = ['name', 'date', 'stimulus1', 'stimulus2',
                             'SVR Eye', 'SVR Emotion', 'SVR Fusion']
            for row, data in enumerate(session_history):
                self.table.insertRow(row)
                for col, key in enumerate(data_key_list):
                    value = data[key]
                    item = QTableWidgetItem(str(value))
                    if col in range(4, 7):  # engagement score
                        item.setTextAlignment(Qt.AlignRight)
                        self.table.setColumnWidth(col, 180)

                    # Set font size for text inside the cells
                    font = QFont()
                    font.setPointSize(12)  # Adjust the font size as needed
                    item.setFont(font)

                    self.table.setItem(row, col, item)

                # Create a button in the last column
                self.view_report_button = QPushButton("View Report", self)
                self.view_report_button.clicked.connect(lambda checked,
                                                        student_index=row,
                                                        button=self.view_report_button:
                                                        self.show_model_menu(student_index, button))
                self.table.setCellWidget(row, len(data_key_list), self.view_report_button)
        except Exception as e:
            print("An error occurred in populate_table:", str(e))

    def show_model_menu(self, student_index, button):
        try:
            # Create Menu
            menu = QMenu(self)

            # Create actions
            eye_action = QAction('SVR Eye', self)
            emotion_action = QAction('SVR Emotion', self)
            fusion_action = QAction('SVR Fusion', self)

            # Connect signals and emit signals
            eye_action.triggered.connect(lambda: self.select_model_signal.emit(student_index, 'SVR Eye'))
            emotion_action.triggered.connect(lambda: self.select_model_signal.emit(student_index, 'SVR Emotion'))
            fusion_action.triggered.connect(lambda: self.select_model_signal.emit(student_index, 'SVR Fusion'))

            # Add actions to menu
            menu.addSection("Select Model")
            menu.addActions([eye_action, emotion_action, fusion_action])

            # Calculate position relative to the parent widget
            pos = button.mapToGlobal(button.rect().bottomLeft())

            # Display menu
            menu.exec_(pos)
        except Exception as e:
            print("An error occurred in show_model_menu:", str(e))

if __name__ == "__main__":
    try:
        with open("../../quiz_data/session_history.yaml", "r", encoding="utf-8") as yaml_file:
            session_history = yaml.load(yaml_file, Loader=yaml.FullLoader)
            if session_history is None:
                raise ValueError("No valid YAML data found in the file.")
    except FileNotFoundError:
        print("YAML file not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading YAML data: {e}")
        sys.exit(1)

    app = QApplication(sys.argv)
    print(session_history)
    screen = SessionHistoryWidget(session_history)
    screen.setGeometry(100, 100, 1000, 800)
    screen.show()
    sys.exit(app.exec_())
