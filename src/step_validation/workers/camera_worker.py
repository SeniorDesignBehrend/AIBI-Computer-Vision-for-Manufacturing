import time

import cv2
import numpy as np
from PySide6.QtCore import QThread, Signal


class CameraWorker(QThread):
    """Captures frames from the camera and emits them as a signal.

    Used for live preview during training (record phase). The consumer
    decides what to do with the frame — display it, buffer it, etc.
    """

    frame_ready = Signal(object)   # emits np.ndarray (BGR)
    camera_error = Signal()        # emitted when camera cannot be opened
    camera_opened = Signal()       # emitted once camera is successfully opened

    def __init__(self, camera_index: int = 0, fps: int = 30, parent=None):
        super().__init__(parent)
        self.camera_index = camera_index
        self._interval = 1.0 / fps
        self._running = False

    def run(self):
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            self.camera_error.emit()
            return

        # Read a first frame to confirm the camera is truly ready
        ret, frame = cap.read()
        if not ret:
            cap.release()
            self.camera_error.emit()
            return

        self.camera_opened.emit()
        self.frame_ready.emit(frame.copy())

        self._running = True
        while self._running:
            ret, frame = cap.read()
            if ret:
                self.frame_ready.emit(frame.copy())
            time.sleep(self._interval)

        cap.release()

    def stop(self):
        self._running = False
        self.wait()
