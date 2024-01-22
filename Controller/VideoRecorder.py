import cv2
from PyQt5.QtCore import QThread


class VideoRecorder(QThread):

    def __init__(self, camera, filename, fps, width, height):
        super().__init__()
        self.record_video_writer = cv2.VideoWriter(filename=filename, fourcc=cv2.VideoWriter_fourcc(*"MJPG"),
                                                   fps=fps, frameSize=(width, height))
        self.is_recording = False
        self.camera = camera

    def run(self):
        print("Start recording")
        self.is_recording = True
        while True:
            if self.is_recording:
                ret, frame = self.camera.read()
                if ret:
                    self.record_video_writer.write(frame)

    def stop(self):
        print("Stop recording")
        self.is_recording = False
        self.record_video_writer.release()
