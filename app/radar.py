from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget


class RadarWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wi-Fi Radar Scanner")
        self.resize(900, 900)

    def paintEvent(self, event):

        painter = QPainter(self)

        # Background
        painter.fillRect(self.rect(), Qt.black)

        # Enable smooth drawing
        painter.setRenderHint(QPainter.Antialiasing)

        # Green pen
        pen = QPen(Qt.green)
        pen.setWidth(2)
        painter.setPen(pen)

        # Center of the window
        center_x = self.width() // 2
        center_y = self.height() // 2

        # Draw 4 radar circles
        for radius in [100, 200, 300, 400]:
            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )

        # Horizontal line
        painter.drawLine(
            center_x - 400,
            center_y,
            center_x + 400,
            center_y
        )

        # Vertical line
        painter.drawLine(
            center_x,
            center_y - 400,
            center_x,
            center_y + 400
        )

        # Direction labels
        painter.drawText(center_x - 5, center_y - 410, "N")
        painter.drawText(center_x - 5, center_y + 425, "S")
        painter.drawText(center_x + 410, center_y + 5, "E")
        painter.drawText(center_x - 420, center_y + 5, "W")