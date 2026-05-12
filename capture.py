# capture.py

import mss
import numpy as np
import cv2


class ScreenCapture:
    def __init__(self):

        self.sct = mss.mss()

        # ЛЕВАЯ ЧАСТЬ ЭКРАНА
        # ТОЛЬКО ОРИГИНАЛЬНЫЙ ТЕКСТ

        self.monitor = {
            "top": 120,
            "left": 20,
            "width": 700,
            "height": 1080
        }

    def grab(self):

        screenshot = self.sct.grab(
            self.monitor
        )

        frame = np.array(screenshot)

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGRA2BGR
        )

        # уменьшаем размер
        # для ускорения OCR

        frame = cv2.resize(
            frame,
            None,
            fx=0.85,
            fy=0.85
        )

        return frame