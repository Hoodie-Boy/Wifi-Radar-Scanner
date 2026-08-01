from dataclasses import dataclass


@dataclass
class WifiNetwork:

    ssid: str
    bssid: str
    signal: int
    frequency: int
    security: str

    # Radar position
    angle: float = 0
    distance: float = 0