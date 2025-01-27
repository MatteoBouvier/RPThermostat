import socket

from .utils import Version, is_valid, get_version
from ..enums import Method

try:
    from typing import Union
except ImportError:
    pass


class Request:
    def __init__(
        self, method: str, path: str, version: Version, headers: dict[str, str]
    ):
        self.method: str = method
        self.path: str = path
        self.version: Version = version
        self.headers: dict[str, str] = headers

    def __repr__(self) -> str:
        r = f"Request <{self.method} {self.path} HTTP/{self.version.major}.{self.version.minor}>"

        for header, value in self.headers.items():
            r += f"\n{header}: {value}"

        return r + "\n"

    @staticmethod
    def from_raw(text: str) -> Union["Request", None]:
        h, *headers = text.split("\n")
        method, path, version = h.split(" ")

        parsed_headers: dict[str, str] = {}
        for line in headers:
            line = line.strip()
            if line:
                name, value = line.split(": ")
                parsed_headers[name] = value

        if not is_valid(method, Method.all()):
            return None

        return Request(method, path, get_version(version), parsed_headers)

    @staticmethod
    def get(s: socket.socket) -> Union["Request", None]:
        data = s.recv(1024).decode("utf-8")
        if not data:
            return None

        return Request.from_raw(data)
