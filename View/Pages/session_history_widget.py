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

from View.Pages.page import Page

# # Initialize Firebase Admin SDK
# cred = credentials.Certificate('C:\\Users\\NEHA\\Downloads\\MLEngagementTool\\firebase.json')
# firebase_admin.initialize_app(cred)



class SessionHistoryWidget(Page):
    select_student_signal = pyqtSignal(dict)  # dict for student data

    def __init__(self):
        super().__init__(heading_text="Analyze Data")
        # create title label
        title_label = QLabel("Session History")
        title_label.setObjectName("analyzeDataTitle")
        title_label.setFixedHeight(180)
        title_label.setAlignment(Qt.AlignCenter)

        # Create table
        self.table = QTableWidget(self)
        self.table.setMinimumWidth(1500)
        self.table.setMinimumHeight(500)
        self.table.setColumnCount(13)
        self.table_header_list = ["Student Name", "Date", "Stimulus 1", "Stimulus 2",
                                  "SVREye S1", "GBEmotion S1", "RFEye S1", "RFFusion S1",
                                  "SVREye S2", "GBEmotion S2", "RFEye S2", "RFFusion S2", ""]
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
        self.main_layout.addWidget(self.header)
        self.main_layout.addWidget(title_label)
        self.main_layout.addStretch(1)
        self.main_layout.addLayout(table_layout)
        self.main_layout.addStretch(1)


    def populate_table(self):
        try:
            # Fetch data from Firestore
            db = firestore.client()
            session_history_ref = db.collection('sessions')
            session_history_docs = session_history_ref.get()
            

            # Populate table with Firestore data
            for doc in session_history_docs:
                data = doc.to_dict()
                date_obj = data.get('date')
                if date_obj:
                    # Extract date components
                    date_str = date_obj.strftime('%B %d, %Y at %I:%M:%S %p %Z')
                else:
                    date_str = ''

                self.table.insertRow(self.table.rowCount())
                self.table.setItem(self.table.rowCount() - 1, 0, QTableWidgetItem(str(doc.id)))
                self.table.setItem(self.table.rowCount() - 1, 1, QTableWidgetItem(date_str))
                self.table.setItem(self.table.rowCount() - 1, 2, QTableWidgetItem(str(data.get('stimulus1', ''))))
                self.table.setItem(self.table.rowCount() - 1, 3, QTableWidgetItem(str(data.get('stimulus2', ''))))
                self.table.setItem(self.table.rowCount() - 1, 4, QTableWidgetItem(str(data.get('SVREye_stimulus1', 0))))
                self.table.setItem(self.table.rowCount() - 1, 5, QTableWidgetItem(str(data.get('GBEmotion_stimulus1', 0))))
                self.table.setItem(self.table.rowCount() - 1, 6, QTableWidgetItem(str(data.get('RFEye_stimulus1', 0))))
                self.table.setItem(self.table.rowCount() - 1, 7, QTableWidgetItem(str(data.get('RFFusion_stimulus1', 0))))
                self.table.setItem(self.table.rowCount() - 1, 8, QTableWidgetItem(str(data.get('SVREye_stimulus2', 0))))
                self.table.setItem(self.table.rowCount() - 1, 9, QTableWidgetItem(str(data.get('GBEmotion_stimulus2', 0))))
                self.table.setItem(self.table.rowCount() - 1, 10, QTableWidgetItem(str(data.get('RFEye_stimulus2', 0))))
                self.table.setItem(self.table.rowCount() - 1, 11, QTableWidgetItem(str(data.get('RFFusion_stimulus2', 0))))

                # Create a button in the last column
                view_report_button = QPushButton("View Report", self)
                view_report_button.clicked.connect(
                    lambda checked, student_index=self.table.rowCount() - 1, button=view_report_button:
                    self.select_student_signal.emit(self.get_student_data_by_index(student_index))
                )
                self.table.setCellWidget(self.table.rowCount() - 1, 12, view_report_button)
        except Exception as e:
            print("An error occurred in populate_table:", str(e))


    def get_student_data_by_index(self, index):
        student_data = {}
        # Assuming column indexes match the order you've added them in self.table_header_list
        student_data['name'] = self.table.item(index, 0).text()
        student_data['date'] = self.table.item(index, 1).text()
        student_data['stimulus1'] = self.table.item(index, 2).text()
        student_data['stimulus2'] = self.table.item(index, 3).text()
        student_data['SVREye_stimulus1'] = self.table.item(index, 4).text()
        student_data['GBEmotion_stimulus1'] = self.table.item(index, 5).text()
        student_data['RFEye_stimulus1'] = self.table.item(index, 6).text()
        student_data['RFFusion_stimulus1'] = self.table.item(index, 7).text()
        student_data['SVREye_stimulus2'] = self.table.item(index, 8).text()
        student_data['GBEmotion_stimulus2'] = self.table.item(index, 9).text()
        student_data['RFEye_stimulus2'] = self.table.item(index, 10).text()
        student_data['RFFusion_stimulus2'] = self.table.item(index, 11).text()
        return student_data