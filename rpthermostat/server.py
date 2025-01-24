import os
import json
import time
import socket
import select

try:
    import network
except ImportError:
    pass

try:
    from typing import Callable
except ImportError:
    pass

from . import config
from .http import Request, Response, Version, get_media_types, KNOWN_MEDIA
from .template import parse


class Server:
    def __init__(self):
        self.listening_conn: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.listening_conn.bind(("", 80))
        self.listening_conn.listen(5)
        self.listening_conn.setblocking(False)

        self.poller: select.poll = select.poll()
        self.poller.register(self.listening_conn, select.POLLIN)

        self.routes: dict[str, tuple[str, Callable[[], str]]] = {}

    def route(
        self, path: str, mime_type: str = "text/html; charset=utf-8"
    ) -> Callable[[Callable[[], str]], None]:
        def inner(callback: Callable[[], str]) -> None:
            self.routes[path] = (mime_type, callback)

        return inner

    @staticmethod
    def connect_wifi(ssid: str, password: str) -> None:
        sta_if = network.WLAN(network.WLAN.IF_STA)
        sta_if.active(True)
        sta_if.connect(ssid, password)

        start = time.time()
        while not sta_if.isconnected():
            if time.time() - start > 30:
                raise OSError("Could not connect to Wifi")

        print("Connected to Wifi")
        print("Using IP address", sta_if.ifconfig()[0])

    def run(self) -> None:
        while True:
            try:
                self.poll()

            except KeyboardInterrupt:
                break

        self.listening_conn.close()

    def poll(self) -> None:
        events = self.poller.poll(-1)

        for conn, mask in events:
            if conn is self.listening_conn:
                self.accept()

            else:
                self.handle_client(conn, mask)

    def accept(self) -> None:
        conn, addr = self.listening_conn.accept()
        print(f"New connection from {addr}")
        conn.setblocking(False)

        events = select.POLLIN | select.POLLOUT
        self.poller.register(conn, events)

    def handle_client(self, conn: socket.socket, mask: int) -> None:
        if mask & select.POLLIN:
            request = Request.get(conn)

            if request is None:
                self.poller.unregister(conn)
                conn.close()
                return

            if mask & select.POLLOUT:
                if request.method == "GET":
                    response = self.get_media(request)

                else:
                    response = Response(Version(1, 1), 405, {}, "")

                response.send(conn)

    def get_media(self, request: Request) -> Response:
        if request.path in self.routes:
            mime_type, body = self.routes[request.path]
            return Response(
                Version(1, 1),
                200,
                {
                    "Transfer-Encoding": "chunked",
                    "Connection": "keep-alive",
                    "Content-Type": mime_type,
                },
                body,
            )

        for accepted_type in get_media_types(request.headers.get("Accept", "*/*")):
            t, st = accepted_type.split("/")
            extension = request.path.split(".")[1]

            if t == "image" and request.path[1:] in os.listdir(
                config.SOURCE + "/assets"
            ):
                body = config.SOURCE + "/assets" + request.path
                headers = {"Content-Type": f"image/{KNOWN_MEDIA[extension]}"}

            elif request.path[1:] in os.listdir(config.SOURCE):
                body = config.SOURCE + request.path
                headers = {
                    "Content-Type": f"text/{KNOWN_MEDIA[extension]}; charset=utf-8"
                }

            else:
                continue

            return Response(
                Version(1, 1),
                200,
                {"Transfer-Encoding": "chunked", "Connection": "keep-alive"} | headers,
                body,
            )

        return Response(Version(1, 1), 404, {}, "")


Server.connect_wifi(config.SSID, config.PASSWORD)
app = Server()


@app.route("/")
def index() -> str:
    return parse(config.SOURCE + "/index.html", current_temp=17.2)


@app.route("/api/temp", "application/json; charset=utf-8")
def api_get_temp() -> str:
    return json.dumps({"min": 16, "max": 19, "current": 17.2})


app.run()
