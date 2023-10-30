import cv2
from deepface import DeepFace
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class EmotionalAnalysis(QThread):
    ImageUpdate = pyqtSignal(QImage)
    emotion_signal = pyqtSignal(str)
   

    def run(self):
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
                self.last_emotion_detection_time = current_time
                
               

    def stop(self):
        self.ThreadActive = False
        self.quit()

# class FacialAnalysis:
#     def __init__(self):
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#         )
#         self.cap = cv2.VideoCapture(0)
#         self.emotion_detection_interval = 5
#         self.last_emotion_detection_time = 0

#     def analyze(self):
#         while True:
#             ret, frame = self.cap.read()
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
            
#             for x, y, w, h in faces:
#                 cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 3)
            
#             current_time = time.time()
#             if current_time - self.last_emotion_detection_time >= self.emotion_detection_interval:
#                 results = DeepFace.analyze(
#                     img_path=frame, actions=["emotion"], enforce_detection=False
#                 )
#                 for result in results:
#                     emotion = result['dominant_emotion']
#                     return emotion
#                 self.last_emotion_detection_time = current_time
