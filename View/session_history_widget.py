import sys
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from View.header_widget import HeaderWidget


class SessionHistoryWidget(QWidget):
    view_report_clicked = pyqtSignal(int)

    def __init__(self, session_history):
        super().__init__()

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
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            ["Student Name", "Date", "Stimulus 1", "Stimulus 2", "Engagement Score", ""]
        )
        self.table.setColumnWidth(4, 200)  # Set width for Column 5
        self.table.setContentsMargins(5, 5, 5, 5)
        self.table.setColumnWidth(5, 200)  # Set width for Column 5

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
        for row, data in enumerate(session_history):
            self.table.insertRow(row)
            for col, key in enumerate(['name', 'date', 'stimulus1', 'stimulus2', 'score']):
                value = data[key]
                item = QTableWidgetItem(str(value))
                if col == 4:  # engagement score
                    item.setTextAlignment(Qt.AlignRight)

                # Set font size for text inside the cells
                font = QFont()
                font.setPointSize(12)  # Adjust the font size as needed
                item.setFont(font)

                self.table.setItem(row, col, item)

            # Create a button in the last column
            button = QPushButton("View Report", self)
            button.clicked.connect(lambda _, r=row: self.view_report_clicked.emit(r))
            self.table.setCellWidget(row, 5, button)


if __name__ == "__main__":
    try:
        with open("../quiz_data/session_history.yaml", "r", encoding="utf-8") as yaml_file:
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
