import sys
from PySide6.QtWidgets import QApplication
from radar import RadarWindow

app = QApplication(sys.argv)

window = RadarWindow()
window.show()

sys.exit(app.exec())