import hashlib
import math


def calculate_position(network):

    # Create a stable angle from MAC address
    value = int(
        hashlib.md5(
            network.bssid.encode()
        ).hexdigest(),
        16
    )


    angle = value % 360


    # Convert signal (-90 to -30)
    # into radar distance (50 to 400)

    signal = network.signal


    distance = (
        (-signal - 30)
        /
        60
    ) * 350


    distance = max(
        50,
        min(distance, 350)
    )


    return angle, distance