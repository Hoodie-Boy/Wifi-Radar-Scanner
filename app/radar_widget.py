from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen
from PySide6.QtWidgets import QWidget
import math
from PySide6.QtGui import QColor
from PySide6.QtCore import Signal

class RadarWidget(QWidget):

    network_clicked = Signal(object)
    def __init__(self):

        from PySide6.QtCore import QTimer
        self.sweep_angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_sweep)
        self.timer.start(20)

        super().__init__()
        self.setWindowTitle("Wi-Fi Radar Scanner")
        self.resize(1000, 1000)
        self.networks = []

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
        for radius in [50, 100, 200, 300]:
            painter.drawEllipse(
                center_x - radius,
                center_y - radius,
                radius * 2,
                radius * 2
            )

        # Horizontal line
        painter.drawLine(
            center_x - 300,
            center_y,
            center_x + 300,
            center_y
        )

        # Vertical line
        painter.drawLine(
            center_x,
            center_y - 300,
            center_x,
            center_y + 300
        )

        # Direction labels
        painter.drawText(center_x - 5, center_y - 310, "N")
        painter.drawText(center_x - 5, center_y + 325, "S")
        painter.drawText(center_x + 310, center_y + 5, "E")
        painter.drawText(center_x - 320, center_y + 5, "W")

        radius = 300
        angle = math.radians(self.sweep_angle)
        end_x = center_x + radius * math.cos(angle)
        end_y = center_y - radius * math.sin(angle)
        pen = QPen(Qt.red)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawLine(
            center_x,
            center_y,
            int(end_x),
            int(end_y)
        )
        self.draw_targets(
            painter,
            center_x,
            center_y
        )
    def update_sweep(self):
        self.sweep_angle -= 2
        if self.sweep_angle >= 360:
            self.sweep_angle = 0
        self.update()

    def set_networks(self, networks):
        self.networks = networks
        self.update()

    def draw_targets(self, painter, center_x, center_y):

        painter.setPen(
            QPen(QColor(255,255,0), 3)
        )


        for network in self.networks:


            angle = math.radians(network.angle)

            x = center_x + network.distance * math.cos(angle)
            y = center_y - network.distance * math.sin(angle)


            self.draw_wifi_icon(
                painter,
                int(x),
                int(y)
            )


            painter.drawText(
                int(x)+15,
                int(y),
                network.ssid
            )
    def draw_wifi_icon(self, painter, x, y):
        pen = QPen(
            QColor(255,116,9)
        )

        pen.setWidth(3)

        painter.setPen(pen)


        # Outer arc
        painter.drawArc(
            x-15,
            y-15,
            30,
            30,
            30*16,
            120*16
        )


        # Middle arc
        painter.drawArc(
            x-10,
            y-10,
            20,
            20,
            30*16,
            120*16
        )


        # Inner arc
        painter.drawArc(
            x-5,
            y-5,
            10,
            10,
            30*16,
            120*16
        )


        # Center point
        painter.setBrush(
            QColor(0,255,0)
        )

        painter.drawEllipse(
            x-3,
            y-3,
            6,
            6
        )
    def mousePressEvent(self, event):

        x_click = event.position().x()
        y_click = event.position().y()


        center_x = self.width() // 2
        center_y = self.height() // 2


        for network in self.networks:

            angle = math.radians(network.angle)

            x = center_x + network.distance * math.cos(angle)

            y = center_y - network.distance * math.sin(angle)


            distance = math.sqrt(
                (x_click-x)**2 +
                (y_click-y)**2
            )


            if distance < 15:

                self.network_clicked.emit(network)

                break