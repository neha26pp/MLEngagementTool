import cv2
from deepface import DeepFace
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class EmotionalAnalysis(QThread):
    '''Facial Emotional Detection with DeepFace'''

    ImageUpdate = pyqtSignal(QImage)
    emotion_signal = pyqtSignal(str)
    detected_emotions = []

    def __init__(self):
        super(EmotionalAnalysis, self).__init__()
        self.record_video_popup = QMessageBox()
        self.record_video_popup.setWindowTitle("Record Video")
        self.record_video_popup.setText("Permission to record video")
        self.record_video_popup.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        self.record_video_popup.setDefaultButton(QMessageBox.Cancel)
        self.record_video_popup.buttonClicked.connect(self.popup_clicked)


    def run(self):
        '''Thread that starts face recognition and emotional analysis'''
        
        self.ThreadActive = True
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        Capture = cv2.VideoCapture(0)
        self.emotion_detection_interval = 2
        self.last_emotion_detection_time = 0

        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
                ConvertToQTFormat = QImage(
                    Image.data,
                    Image.shape[1],
                    Image.shape[0],
                    Image.shape[1] * 3,
                    QImage.Format_RGB888,
                )
                Pic = ConvertToQTFormat.scaled(640, 480, Qt.KeepAspectRatio)

               
                self.ImageUpdate.emit(Pic)
               

                current_time = time.time()
            if current_time - self.last_emotion_detection_time >= self.emotion_detection_interval:
                results = DeepFace.analyze(
                    img_path=frame, actions=["emotion"], enforce_detection=False
                )
                for result in results:
                    emotion = result['dominant_emotion']
                    self.emotion_signal.emit(emotion)
                    print("EMOOOOOOTION" , emotion)
                    self.detected_emotions.append(emotion)
                self.last_emotion_detection_time = current_time
                
               

    def stop(self):
        self.ThreadActive = False
        self.quit()
    
    def popup_clicked(self, button):
        if self.record_video_popup.isHidden():
            return  # Ignore clicks if the popup is hidden

        if button.text() == "Yes":
            self.record_video_popup.close()


