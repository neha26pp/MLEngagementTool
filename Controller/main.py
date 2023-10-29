import sys
import cv2
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import emotional_analysis
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()  # Call the superclass's __init__ method properly

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel(self)
        self.VBL.addWidget(self.FeedLabel)

        self.CancelBTN = QPushButton("Cancel", self)
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        
        global emotion
        self.emotion_label = QLabel("Emotion: ")
        self.VBL.addWidget(self.emotion_label)

        self.setLayout(self.VBL)

        self.EmotionalAnalysis = emotional_analysis.EmotionalAnalysis()
        self.EmotionalAnalysis.ImageUpdate.connect(self.ImageUpdateSlot)
        self.EmotionalAnalysis.emotion_signal.connect(self.EmotionUpdateSlot)
        self.EmotionalAnalysis.start()

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))
    
    def EmotionUpdateSlot(self, emotion):
        if self.emotion_label is not None:
                self.emotion_label.setText(f"Emotion: {emotion}")

    def CancelFeed(self):
        self.EmotionalAnalysis.stop()



if __name__ == "__main__":
    App = QApplication(sys.argv)
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())


# class EmotionAnalyzer(QThread):
#     emotion_signal = pyqtSignal(str)
#     frame_signal = pyqtSignal(QPixmap)

#     def __init__(self, facial_analyzer):
#         super().__init__()
#         self.facial_analyzer = facial_analyzer

#     def run(self):
#         while True:
#             emotion = self.facial_analyzer.analyze()
#             self.emotion_signal.emit(emotion)

# class VideoDisplay(QThread):
#     frame_signal = pyqtSignal(QPixmap)
#     def __init__(self):
#         super().__init()
#         self.cap = cv2.VideoCapture(0)

#     def run(self):
#         while True:
#             ret, frame = self.cap.read()
#             if ret:
#                 frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 h, w, ch = frame.shape
#                 bytes_per_line = ch * w
#                 q_img = QImage(frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
#                 self.frame_signal.emit(QPixmap.fromImage(q_img))

# def update_emotion(emotion):
#     if emotion_label is not None:
#         emotion_label.setText(f"Emotion: {emotion}")


# def update_frame(frame):
#     video_label.setPixmap(frame)


# def main():
#     app = QApplication(sys.argv)
#     window = QMainWindow()
#     window.setWindowTitle("Facial Emotion Analysis")

#     central_widget = QWidget()
#     window.setCentralWidget(central_widget)

#     layout = QVBoxLayout(central_widget)

#     global video_label
#     video_label = QLabel()
#     global emotion_label
#     emotion_label = QLabel("Emotion: ")
#     layout.addWidget(video_label)
#     layout.addWidget(emotion_label)

#     facial_analyzer = facial_analysis.FacialAnalysis()
#     emotion_analyzer = EmotionAnalyzer(facial_analyzer)
#     emotion_analyzer.emotion_signal.connect(update_emotion)
#     emotion_analyzer.frame_signal.connect(update_frame)
#     emotion_analyzer.start()

#     window.show()
#     app.exec_()


# if __name__ == "__main__":
#     main()
