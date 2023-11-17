import cv2
from deepface import DeepFace
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class EmotionalAnalysis(QThread):
    '''Facial Emotional Detection with DeepFace'''

    # ImageUpdate = pyqtSignal(QImage)
    # emotion_signal = pyqtSignal(str)
    detected_emotions = []
    current_time = 0
    

    def __init__(self):
        super(EmotionalAnalysis, self).__init__()
       
        
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.capture = cv2.VideoCapture(0)
        self.emotion_detection_interval = 0.5
        self.last_emotion_detection_time = 0
        self.ThreadActive = False



    def run(self):
        '''Thread that starts face recognition and analysis'''
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame = self.capture.read()
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

               
                # self.ImageUpdate.emit(Pic) # show opencv face feed
               

                self.current_time = time.time()
            if self.current_time - self.last_emotion_detection_time >= self.emotion_detection_interval:
                results = DeepFace.analyze(
                    img_path=frame, actions=["emotion"], enforce_detection=False
                )
                for result in results:
                    emotion = result['dominant_emotion']
                    # self.emotion_signal.emit(emotion)
                    print("EMOTION DETECTED: " , emotion)
                    self.detected_emotions.append(emotion)
                self.last_emotion_detection_time = self.current_time
                
               

    def stop(self):
        self.ThreadActive = False
        self.quit()

    def get_activity(self):
        return self.ThreadActive
    




# import cv2
# import time
# import threading
# from PyQt5.QtCore import Qt, pyqtSignal, QThread
# from PyQt5.QtGui import QImage
# from PyQt5.QtWidgets import QMessageBox
# from deepface import DeepFace

# class EmotionalAnalysis(QThread):

#     ImageUpdate = pyqtSignal(QImage)
#     emotion_signal = pyqtSignal(str)

#     def __init__(self):
#         super(EmotionalAnalysis, self).__init__()
#         self.ThreadActive = True
#         self.face_cascade = cv2.CascadeClassifier(
#             cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#         )
#         self.emotion_detection_interval = 2
#         self.last_emotion_detection_time = 0

#     def run(self):
#         '''Thread that starts face recognition and emotional analysis'''
#         Capture = cv2.VideoCapture(0)
#         print("here")
#         while self.ThreadActive:
#             ret, frame = Capture.read()
#             if ret:
#                 Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#                 ConvertToQTFormat = QImage(
#                     Image.data,
#                     Image.shape[1],
#                     Image.shape[0],
#                     Image.shape[1] * 3,
#                     QImage.Format_RGB888,
#                 )
#                 Pic = ConvertToQTFormat.scaled(640, 480, Qt.KeepAspectRatio)

#                 self.ImageUpdate.emit(Pic)

#                 current_time = time.time()
#                 if current_time - self.last_emotion_detection_time >= self.emotion_detection_interval:
#                     results = DeepFace.analyze(
#                         img_path="",  # Pass a valid image path here
#                         actions=["emotion"],
#                         enforce_detection=False
#                     )
#                     emotion = results['dominant_emotion']
#                     self.emotion_signal.emit(emotion)
#                     print("EMOTION DETECTED:", emotion)
#                     self.last_emotion_detection_time = current_time

#     def stop(self):
#         self.ThreadActive = False
#         self.quit()

