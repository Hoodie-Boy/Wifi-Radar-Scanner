import time
import pywifi
from pywifi import const
from models import WifiNetwork
from utils import calculate_position

class WifiScanner:
    def __init__(self):
        wifi = pywifi.PyWiFi()
        self.interface = wifi.interfaces()[0]

    def scan(self):
        print("Starting scan...")
        self.interface.scan()
        time.sleep(2)
        results = self.interface.scan_results()
        print("Number of networks found:", len(results))
        networks = []
        for wifi in results:
            print(
                wifi.ssid,
                wifi.signal,
                wifi.freq
            )
            if wifi.akm:
                security = "Secured"
            else:
                security = "Open"
            network = WifiNetwork(
                ssid=wifi.ssid,
                bssid=wifi.bssid,
                signal=wifi.signal,
                frequency=wifi.freq,
                security=security
            )
            network.angle, network.distance = calculate_position(network)
            networks.append(network)

        return networks