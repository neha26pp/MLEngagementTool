import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import emotional_analysis
import os

view_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "View"))
sys.path.append(view_directory)

import video
import gui

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent



class MainWindow(QWidget):
    ''' Main Controller class
        Communicates with all other classes
    '''
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.gui = gui.Gui(self)
        
        self.VBL.addWidget(self.gui)

        self.setLayout(self.VBL)

        
        

    def image_update_slot(self, Image):
        '''function to display the opencv video feed (face)'''
        self.feed_label.setPixmap(QPixmap.fromImage(Image))

    def emotion_update_slot(self, emotion):
        '''function to diplay the detected emotion'''
        self.emotion_label.setText(f"Emotion: {emotion}")

    def cancel_feed(self):
        '''function to stop face recognition and analysis'''
        self.emotional_analysis.stop()
    
    def collectDataBtn_pressed(self):

        '''Start collecting data (experiment)'''

        print("collecting data")

        self.gui.hide()


        self.video= video.Video()
        self.emotional_analysis= emotional_analysis.EmotionalAnalysis()
        self.video_layout = QHBoxLayout()

        self.feed_label = QLabel(self)
        self.video_layout.addWidget(self.feed_label)

        self.VBL.addLayout(self.video_layout)

        self.cancel_btn = QPushButton("Cancel", self)
        self.cancel_btn.clicked.connect(self.cancel_feed)
        self.VBL.addWidget(self.cancel_btn)


        self.emotion_label = QLabel("Emotion: ")
        self.VBL.addWidget(self.emotion_label)

        self.emotional_analysis.ImageUpdate.connect(self.image_update_slot)
        self.emotional_analysis.emotion_signal.connect(self.emotion_update_slot)


        self.webview = self.video.webview
        self.video_layout.addWidget(self.webview)
        self.emotional_analysis.start()

    
    def analyzeDataBtn_pressed(self):
        '''Analyze previously collected data'''
        print("analyzing data")



if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())


