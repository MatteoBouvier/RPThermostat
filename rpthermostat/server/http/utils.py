import socket

try:
    from typing import NamedTuple

    class Version(NamedTuple):
        major: int
        minor: int

except ImportError:
    from collections import namedtuple

    Version = namedtuple("Version", ("major", "minor"))  # pyright: ignore[reportAssignmentType]
    BrokenPipeError = OSError
    ConnectionResetError = OSError


def get_version(v: str) -> Version:
    if not v.startswith("HTTP/"):
        raise ValueError

    M, m = v[5:].split(".")
    return Version(int(M), int(m))


def is_valid(s: str, valid: tuple[str, ...]) -> bool:
    return s in valid


def get_media_types(MIME_type: str) -> list[str]:
    types = [t.split(";q=") if ";" in t else (t, 1) for t in MIME_type.split(",")]
    return [t for (t, _) in sorted(types, key=lambda x: float(x[1]))]


def safe_send(s: socket.socket, data: bytes) -> int:
    try:
        return s.send(data)

    except (BrokenPipeError, ConnectionResetError):
        return -1


def html_document(title: str, *, head: str = "", body: str = "") -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <title>{title}</title>
  {head}
</head>
<body>
  {body}
</body>
</html>"""
