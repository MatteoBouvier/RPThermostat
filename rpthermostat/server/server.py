import os
import re
import socket
import select

from .utils import print_exception

from .enums import MIMEType, Code, Marker, Method
from .http import Request, Response, get_media_types

try:
    from typing import Callable
except ImportError:
    pass


BRACKETS = re.compile("[{}]")


class Nice:
    def __init__(
        self, *, port: int = 80, source_folder: str = ".", use_micro_python: bool = True
    ):
        self.source_folder: str = source_folder

        self.listening_conn: socket.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        self.listening_conn.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listening_conn.bind(("", port))
        self.listening_conn.listen(5)
        self.listening_conn.setblocking(False)

        if use_micro_python:
            self.poller: select.poll | None = select.poll()
            self.poller.register(self.listening_conn, select.POLLIN)

        else:
            self.poller = None

        self.sockets: set[socket.socket] = set()
        self.sockets.add(self.listening_conn)

        self.routes: dict[
            Method,
            dict[tuple[tuple[str, ...], ...], tuple[MIMEType, Callable[..., str]]],
        ] = {
            Method.GET: {},
            Method.POST: {},
        }

    @staticmethod
    def _parse_path(path: str) -> tuple[tuple[str, ...], ...]:
        return tuple(
            tuple(BRACKETS.sub("?", part).split("?"))
            for part in path.rstrip("/").split("/")
        )

    def get(
        self, path: str, mime_type: MIMEType = MIMEType.html
    ) -> Callable[[Callable[..., str]], None]:
        def inner(callback: Callable[..., str]) -> None:
            self.routes[Method.GET][Nice._parse_path(path)] = (mime_type, callback)

        return inner

    def post(
        self, path: str, mime_type: MIMEType = MIMEType.NONE
    ) -> Callable[[Callable[[Request], str]], None]:
        def inner(callback: Callable[[Request], str]) -> None:
            self.routes[Method.POST][Nice._parse_path(path)] = (mime_type, callback)

        return inner

    @staticmethod
    def _match_one_route(
        route: tuple[tuple[str, ...], ...], req_route: list[str]
    ) -> tuple[bool, tuple[str, ...]]:
        args: tuple[str, ...] = ()

        if len(route) != len(req_route):
            return False, ()

        for part, req_part in zip(route, req_route):
            if len(part) == 1 and part[0] == req_part:
                continue

            elif len(part) == 3:
                args = args + (req_part,)
                continue

            return False, ()

        return True, args

    def match_route(
        self, method: Method, req_route: str
    ) -> tuple[tuple[tuple[str, ...], ...] | None, tuple[str, ...]]:
        req_parts = req_route.split("/")

        for route in self.routes[method]:
            matched, args = Nice._match_one_route(route, req_parts)
            if matched:
                return route, args

        return None, ()

    def poll(self) -> None:
        if self.poller is None:
            ready_to_read, ready_to_write, _ = select.select(
                self.sockets, self.sockets, []
            )

            for conn in ready_to_read:
                if conn is self.listening_conn:
                    self.accept()

                else:
                    mask = (
                        select.POLLIN | select.POLLOUT
                        if conn in ready_to_write
                        else select.POLLIN
                    )
                    self.handle_client(conn, mask)

        else:
            events: list[tuple[socket.socket, int]] = self.poller.poll(-1)  # pyright: ignore[reportAssignmentType]

            for conn, mask in events:
                if conn is self.listening_conn:
                    self.accept()

                else:
                    self.handle_client(conn, mask)

    def run(self) -> None:
        while True:
            try:
                self.poll()

            except KeyboardInterrupt:
                break

        self.listening_conn.close()

    def accept(self) -> None:
        conn, addr = self.listening_conn.accept()
        print(f"New connection from {addr}")
        conn.setblocking(False)

        events = select.POLLIN | select.POLLOUT
        if self.poller is None:
            self.sockets.add(conn)
        else:
            self.poller.register(conn, events)

    def handle_client(self, conn: socket.socket, mask: int) -> None:
        if mask & select.POLLIN:
            request = Request.get(conn)

            if request is None:
                if self.poller is None:
                    self.sockets.remove(conn)
                else:
                    self.poller.unregister(conn)

                conn.close()
                return

            if mask & select.POLLOUT:
                if request.method == "GET":
                    matched_route, args = self.match_route(Method.GET, request.path)
                    if matched_route is not None:
                        mime_type, callback = self.routes[Method.GET][matched_route]

                        try:
                            body = callback(*args)
                        except Exception as err:
                            response = Response.InternalServerError(
                                print_exception(err), MIMEType.html
                            )
                        else:
                            response = Response.OK(body, mime_type)

                    else:
                        response = self.get_media(request)

                elif request.method == "POST":
                    matched_route, args = self.match_route(Method.POST, request.path)
                    if matched_route is not None:
                        mime_type, callback = self.routes[Method.POST][matched_route]

                        try:
                            body = callback(request)
                        except Exception as err:
                            response = Response.InternalServerError(
                                print_exception(err), MIMEType.html
                            )
                        else:
                            response = Response.OK(body or "", mime_type)

                    else:
                        response = Response.empty(Code.e404)

                else:
                    response = Response.empty(Code.e405)

                response.send(conn)

    def get_media(self, request: Request) -> Response:
        requested_file_name = request.path[1:]
        extension = request.path.split(".")[1]
        mime_type = MIMEType.match(extension)

        if mime_type is None:
            return Response.empty(Code.e415)

        for accepted_type in get_media_types(request.headers.get("Accept", "*/*")):
            if MIMEType.is_asset(accepted_type) and requested_file_name in os.listdir(
                self.source_folder + "/assets"
            ):
                body = (
                    Marker.FILE + self.source_folder + "/assets/" + requested_file_name
                )

            elif requested_file_name in os.listdir(self.source_folder):
                body = Marker.FILE + self.source_folder + "/" + requested_file_name

            else:
                continue

            return Response.OK(body, mime_type)

        return Response.empty(Code.e404)
