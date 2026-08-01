from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame
)

from radar_widget import RadarWidget
from scanner import WifiScanner
from PySide6.QtCore import QTimer
from wifi_worker import WifiWorker
from PySide6.QtCore import Qt

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Wi-Fi Radar Scanner")
        self.resize(1000, 700)

        # ======================
        # Main Layout
        # ======================

        main_layout = QHBoxLayout(self)

        # ======================
        # Left Information Panel
        # ======================

        info_panel = QFrame()
        info_panel.setFixedWidth(280)

        info_panel.setStyleSheet("""
            QFrame{
                background-color:#202020;
                border:2px solid #00ff00;
                border-radius:10px;
            }

            QLabel{
                color:#00ff00;
                font-size:14px;
            }
        """)

        info_layout = QVBoxLayout(info_panel)

        title = QLabel("Wi-Fi Information")
        self.status = QLabel("Status : Ready")
        self.networks = QLabel("Networks : 0")
        self.selected = QLabel("Selected : None")
        self.signal = QLabel("Signal : ---")
        self.frequency = QLabel("Frequency : ---")
        self.security = QLabel("Security : ---")

        info_layout.addWidget(title)
        info_layout.addSpacing(20)

        info_layout.addWidget(self.status)
        info_layout.addWidget(self.networks)
        info_layout.addWidget(self.selected)
        info_layout.addWidget(self.signal)
        info_layout.addWidget(self.frequency)
        info_layout.addWidget(self.security)

        info_layout.addStretch()


        # ======================
        # Developer Information
        # ======================

        developer_panel = QFrame()

        developer_panel.setStyleSheet("""
            QFrame{
                background-color:#101010;
                border:1px solid #00aa00;
                border-radius:8px;
            }

            QLabel{
                color:#00ff00;
                font-size:12px;
            }
        """)


        developer_layout = QVBoxLayout(developer_panel)

        developer_title = QLabel("Developer Information")
        developer_title.setAlignment(Qt.AlignCenter)
        developer_info = QLabel(
            """
Project:
    Wi-Fi Radar Scanner
            
Developer:
    Amir Mohammadi (Nirad Team Leader)        
            """
        )


        developer_info.setWordWrap(True)


        developer_layout.addWidget(developer_title)
        developer_layout.addWidget(developer_info)
        info_layout.addWidget(developer_panel)
        # ======================
        # Radar
        # ======================
        self.radar = RadarWidget()
        self.radar.network_clicked.connect(
        self.show_network_info
        )
        self.selected_network = None
        
        self.worker = WifiWorker()
        self.worker.networks_updated.connect(
            self.update_radar
        )
        self.worker.start()

        # ======================
        # Add to Main Layout
        # ======================

        main_layout.addWidget(info_panel)
        main_layout.addWidget(self.radar)
    def update_radar(self, networks):

        self.radar.set_networks(networks)


        self.networks.setText(
            f"Networks : {len(networks)}"
        )


        # If selected network disappeared
        if self.selected_network:

            found = False

            for net in networks:

                if net.bssid == self.selected_network.bssid:
                    found = True
                    break


            if not found:
                self.selected_network = None
                self.clear_information()

    # def closeEvent(self, event):
    #     self.worker.stop()
    #     event.accept()

    def show_network_info(self, network):
        self.selected_network = network

        self.selected.setText(
            f"Selected : {network.ssid}"
        )

        self.signal.setText(
            f"Signal : {network.signal} dBm"
        )

        self.frequency.setText(
            f"Frequency : {network.frequency}"
        )

        self.security.setText(
            f"Security : {network.security}"
        )
    def clear_information(self):

        self.selected.setText(
            "Selected : None"
        )

        self.signal.setText(
            "Signal : ---"
        )

        self.frequency.setText(
            "Frequency : ---"
        )

        self.security.setText(
            "Security : ---"
        )
    def closeEvent(self, event):

        if self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()
