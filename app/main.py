import sys
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from wifi_worker import WifiWorker

app = QApplication(sys.argv)

window = MainWindow()

window.show()

sys.exit(app.exec())