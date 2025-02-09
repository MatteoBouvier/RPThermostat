import io
import socket

from .utils import Version, safe_send
from ..enums import Code, Header, MIMEType, Marker


class Response:
    def __init__(
        self,
        version: Version,
        status_code: Code,
        headers: dict[Header, str],
        body: str,
    ):
        self.version: Version = version
        self.status_code: Code = status_code
        self.headers: dict[Header, str] = headers
        self.body: str = body

    def __repr__(self) -> str:
        r = f"Response <HTTP/{self.version.major}.{self.version.minor} {Code.get_value(self.status_code)} {self.status_code}>\n"

        for header, value in self.headers.items():
            r += f"{header}: {value}\n"

        return r + ("(...)" if callable(self.body) else self.body) + "\n"

    @classmethod
    def empty(cls, status_code: Code) -> "Response":
        return Response(Version(1, 1), status_code, {Header.ContentLength: "0"}, "")

    @classmethod
    def OK(cls, body: str, mime_type: MIMEType) -> "Response":
        headers: dict[Header, str] = {
            Header.TransferEncoding: Header.TransferEncodingV.Chunked,
            Header.Connection: Header.ConnectionV.KeepAlive,
        }

        if mime_type != MIMEType.NONE:
            headers[Header.ContentType] = mime_type

        return Response(
            Version(1, 1),
            Code.s200,
            headers,
            body,
        )

    @classmethod
    def InternalServerError(cls, body: str, mime_type: MIMEType) -> "Response":
        return Response(
            Version(1, 1),
            Code.e500,
            {
                Header.ContentType: mime_type,
                Header.ContentLength: str(len(body.encode("utf-8"))),
            },
            body,
        )

    def send(self, s: socket.socket) -> None:
        """Send response over a socket."""
        has_body = bool(len(self.body))
        if not has_body:
            data = io.BytesIO()

        elif self.body.startswith(Marker.FILE):
            data = open(self.body[6:], "rb")

        else:
            data = io.BytesIO(self.body.encode("utf-8"))

        resp = f"HTTP/{self.version.major}.{self.version.minor} {Code.get_value(self.status_code)} {self.status_code}\r\n"

        for header, value in self.headers.items():
            resp += f"{header}: {value}\r\n"

        resp += "\r\n"

        _ = s.send(resp.encode())

        try:
            if has_body:
                if self.headers.get(Header.TransferEncoding) == "chunked":
                    chunk = data.read(1024)
                    while chunk:
                        # Send the size of the chunk in hexadecimal, followed by the chunk itself
                        _ = safe_send(
                            s, f"{len(chunk):X}\r\n".encode("utf-8") + chunk + b"\r\n"
                        )

                        chunk = data.read(1024)

                    _ = safe_send(
                        s, b"0\r\n\r\n"
                    )  # Send the zero-length chunk to indicate end

                else:
                    # determine length from the Content-Length
                    assert self.headers.get(Header.ContentLength) is not None, (
                        "No Content-Length defined"
                    )
                    _ = safe_send(s, data.read())

        finally:
            data.close()
