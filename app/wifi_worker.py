from PySide6.QtCore import QThread, Signal
from scanner import WifiScanner
import time


class WifiWorker(QThread):

    networks_updated = Signal(list)


    def __init__(self):
        super().__init__()

        self.running = True
        self.scanner = WifiScanner()
        self.network_memory = {}
    def run(self):

        while self.running:

            networks = self.scanner.scan()

            if not self.running:
                break

            self.networks_updated.emit(networks)


            # interruptible delay
            for _ in range(50):

                if not self.running:
                    break

                time.sleep(0.1)



    def stop(self):

        self.running = False