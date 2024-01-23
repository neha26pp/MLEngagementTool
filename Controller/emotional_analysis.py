from datetime import datetime

import cv2
from deepface import DeepFace
import time
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from Controller.VideoRecorder import VideoRecorder


class EmotionalAnalysis(QThread):
    '''Facial Emotional Detection with DeepFace'''

    # ImageUpdate = pyqtSignal(QImage)
    # emotion_signal = pyqtSignal(str)
    detected_emotions = []
    current_time = 0

    def __init__(self, camera):
        super(EmotionalAnalysis, self).__init__()
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        self.capture = camera
        self.emotion_detection_interval = 0.5
        self.last_emotion_detection_time = 0
        self.ThreadActive = False
        self.video_recorder = None

        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))

        if self.fps <= 0:
            num_frames = 120
            elapsed_times = []

            for _ in range(num_frames):
                start_time = time.time()
                _, _ = self.capture.read()
                end_time = time.time()
                elapsed_times.append(end_time - start_time)
                # print(end_time - start_time)

            #print(sum(elapsed_times), num_frames)


            if sum(elapsed_times) != 0:
                self.fps = 1 / (sum(elapsed_times) / num_frames)
            print(sum(elapsed_times))
            print(f"actual_fps: {self.fps}")


    def run(self):
        '''Thread that starts face recognition and analysis'''
        self.ThreadActive = True

        width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        file_name = f"../quiz_data/video_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.avi"
        self.video_recorder = VideoRecorder(self.capture, file_name, int(self.fps), width, height)
        self.video_recorder.start()

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
                    print("EMOTION DETECTED: ", emotion)
                    self.detected_emotions.append(emotion)
                self.last_emotion_detection_time = self.current_time

    def stop(self):
        self.ThreadActive = False
        self.quit()

        if self.video_recorder is not None:
            self.video_recorder.stop()

        if len(self.detected_emotions) > 1:
            self.save_emotions()

    def get_activity(self):
        return self.ThreadActive

    def save_emotions(self):
        # Get the current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Save emotion list as file
        with open(f"../quiz_data/emotional_analysis/emotional_analysis_{current_datetime}.txt", 'w') as file:
            for emotion in self.detected_emotions:
                file.write("%s\n" % emotion)

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
