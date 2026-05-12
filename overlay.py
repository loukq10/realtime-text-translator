# overlay.py

from PyQt6.QtWidgets import (
    QApplication,
    QWidget
)

from PyQt6.QtCore import (
    Qt,
    QTimer
)

from PyQt6.QtGui import (
    QPainter,
    QColor,
    QFont
)

import sys


class OverlayWindow(QWidget):
    def __init__(self, shared_data):

        super().__init__()

        self.shared_data = shared_data

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            |
            Qt.WindowType.WindowStaysOnTopHint
            |
            Qt.WindowType.Tool
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TranslucentBackground
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_TransparentForMouseEvents
        )

        self.showFullScreen()

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update
        )

        self.timer.start(50)

    def paintEvent(self, event):

        painter = QPainter(self)

        font = QFont(
            "Arial",
            22
        )

        painter.setFont(font)

        for item in self.shared_data[
            "translations"
        ].values():

            x = item["x"]

            y = item["y"]

            text = item["translation"]

            # SHADOW

            painter.setPen(
                QColor(0, 0, 0)
            )

            painter.drawText(
                x + 952,
                y + 2,
                text
            )

            # MAIN

            painter.setPen(
                QColor(
                    255,
                    255,
                    255
                )
            )

            painter.drawText(
                x + 950,
                y,
                text
            )


def run_overlay(shared_data):

    app = QApplication(sys.argv)

    window = OverlayWindow(
        shared_data
    )

    sys.exit(app.exec())