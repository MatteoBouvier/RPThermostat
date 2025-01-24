from collections import namedtuple

Methods = ("GET")
Headers = ("Host", "User-Agent", "Accept", "Accept-Language", "Accept-Encoding", "Connection", "Upgrade-Insecure-Requests", "Priority", "Referer")
Codes = {
    200: "OK",
    404: "Not Found",
    405: "Method Not Allowed",
}
KNOWN_MEDIA = {
    "ico": "x-icon",
    "html": "html",
    "css": "css",
    "js": "javascript",
}

Version = namedtuple("Version", ("major", "minor"))


def get_version(v: str) -> Version:
    if not v.startswith("HTTP/"):
        raise ValueError
    
    M, m = v[5:].split('.')
    return Version(int(M), int(m))


def validate(s: str, valid: tuple[str, ...]) -> str:
    if s not in valid:
        raise RuntimeError(f"Invalid value {s} not in {valid}")
    
    return s


def get_media_types(MIME_type: str) -> list[str]:
    types = [t.split(";q=") if ";" in t else (t, 1) for t in MIME_type.split(",")]
    return [t for (t, _) in sorted(types, key=lambda x: float(x[1]))]