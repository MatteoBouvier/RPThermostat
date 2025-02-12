import time
import network


def connect_wifi(ssid: str, password: str, timeout: int | None = 30) -> None:
    """Attempt connecting to the wifi using SSID and password.
    Raises an OSError if connection could not be established after `timeout` seconds, if timeout is not set to None."""
    sta_if = network.WLAN(network.WLAN.IF_STA)  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue, reportUnknownArgumentType]
    sta_if.active(True)
    sta_if.connect(ssid, password)  # pyright: ignore[reportUnknownMemberType]

    start = time.time()
    while not sta_if.isconnected():
        if timeout is not None and (time.time() - start) > timeout:
            raise OSError("Could not connect to Wifi")

    print("Connected to Wifi")
    print("Using IP address", sta_if.ifconfig()[0])  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
