import sys
import yaml
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from View.Components.header_widget import HeaderWidget
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Initialize Firebase Admin SDK
cred = credentials.Certificate('C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\View\\Pages\\firebase.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

class SessionHistoryWidget(QWidget):
    select_model_signal = pyqtSignal(dict, str)  # dict for student data, str for the model type

    

    def __init__(self):
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
        self.table.setColumnCount(8)
        self.table_header_list = ["Student Name", "Date", "Stimulus 1", "Stimulus 2",
                                  "Score(SVR Eye)", "Score(SVR Emotion)", "Score(SVR Fusion)", ""]
        self.table.setHorizontalHeaderLabels(self.table_header_list)
        self.table.setContentsMargins(5, 5, 5, 5)
        self.table.setColumnWidth(len(self.table_header_list) - 1, 200)  # Set width for the last Column

        # Populate table with student data
        self.populate_table()

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

    def populate_table(self):
        try:
            # Fetch data from Firestore
            session_history_ref = db.collection('test_collection')
            session_history_docs = session_history_ref.get()

            # Populate table with Firestore data
            for doc in session_history_docs:
                data = doc.to_dict()
                date_str = data['date'].strftime('%m/%d/%Y')
                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(doc.id)))
                self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(date_str))
                self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str(data['stimulus1'])))
                self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(str(data['stimulus2'])))
                self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem(str(data['eyeScore'])))
                self.table.setItem(self.table.rowCount() - 1, 5, QTableWidgetItem(str(data['emotionScore'])))
                self.table.setItem(self.table.rowCount() - 1, 6, QTableWidgetItem(str(data['fusionScore'])))

               # Create a button in the last column
                view_report_button = QPushButton("View Report", self)
                view_report_button.clicked.connect(
                    lambda checked, student_index=self.table.rowCount() - 1, button=view_report_button:
                    self.show_model_menu(student_index, button)
                )
                self.table.setCellWidget(self.table.rowCount() - 1, 7, view_report_button)
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
            eye_action.triggered.connect(lambda: self.emit_signal_with_data(student_index, 'SVR Eye'))
            emotion_action.triggered.connect(lambda: self.emit_signal_with_data(student_index, 'SVR Emotion'))
            fusion_action.triggered.connect(lambda: self.emit_signal_with_data(student_index, 'SVR Fusion'))


            # Add actions to menu
            menu.addSection("Select Model")
            menu.addActions([eye_action, emotion_action, fusion_action])

            # Calculate position relative to the parent widget
            pos = button.mapToGlobal(button.rect().bottomLeft())

            # Display menu
            menu.exec_(pos)
        except Exception as e:
            print("An error occurred in show_model_menu:", str(e))

    def emit_signal_with_data(self, student_index, model_type):
        # Assuming you have a method to fetch student data by index
        print(model_type)
        student_data = self.get_student_data_by_index(student_index, model_type)
        self.select_model_signal.emit(student_data, model_type)

    def get_student_data_by_index(self, index, model_type):
        student_data = {}
        # Assuming column indexes match the order you've added them in self.table_header_list
        student_data['name'] = self.table.item(index, 0).text()
        student_data['date'] = self.table.item(index, 1).text()
        student_data['stimulus1'] = self.table.item(index, 2).text()
        student_data['stimulus2'] = self.table.item(index, 3).text()
        student_data['eyeScore'] = self.table.item(index, 4).text()
        student_data['emotionScore'] = self.table.item(index, 5).text()
        student_data['fusionScore'] = self.table.item(index, 6).text()
        if model_type == 'SVR Eye':
            student_data['Model'] = 'SVR Eye'
        elif model_type == 'SVR Emotion':
            student_data['Model'] = 'SVR Emotion'
        elif model_type == 'SVR Fusion':
            student_data['Model'] = 'SVR Fusion'
        return student_data


if __name__ == "__main__":

    app = QApplication(sys.argv)
    print(session_history)
    screen = SessionHistoryWidget(session_history)
    screen.setGeometry(100, 100, 1000, 800)
    screen.show()
    sys.exit(app.exec_())
