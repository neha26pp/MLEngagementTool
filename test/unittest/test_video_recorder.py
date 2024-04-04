import unittest
import numpy as np
import time
from unittest.mock import MagicMock
from Controller.video_recorder import VideoRecorder  # Import VideoRecorder from your module


class TestVideoRecorder(unittest.TestCase):
    def setUp(self):
        # Create a mock camera object
        self.mock_camera = MagicMock()
        self.mock_camera.read.return_value = True, np.zeros((480, 640, 3), dtype=np.uint8)  # Simulate a frame

        # Create a VideoRecorder object with mock camera
        self.recorder = VideoRecorder(camera=self.mock_camera, filename="test.avi", fps=30, width=640, height=480)

    def test_run_video_recorder(self):
        # Start recording
        self.recorder.start()

        # Wait for a while to simulate recording
        time.sleep(1)

        # Check if the recording was started
        self.assertTrue(self.recorder.is_recording)

        # Stop recording
        self.recorder.stop()

    def test_stop_video_recorder(self):
        # Start recording
        self.recorder.is_recording = True

        # Stop recording
        self.recorder.stop()

        # Check if is_recording is False after stopping
        self.assertFalse(self.recorder.is_recording)


if __name__ == '__main__':
    unittest.main()
