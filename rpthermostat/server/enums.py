from .lib import StrEnum

try:
    from typing import Union
except ImportError:
    pass


class MIMEType(StrEnum):
    NONE = ""
    html = "text/html; charset=utf-8"
    css = "text/css; charset=utf-8"
    js = "text/javascript; charset=utf-8"
    json = "application/json; charset=utf-8"
    ico = "image/x-icon"

    @staticmethod
    def is_asset(typ: str) -> bool:
        t, sub_t = typ.split("/")

        return t in ("image", "*") or sub_t in ("css", "javascript")

    @classmethod
    def match(cls, extension: str) -> Union["MIMEType", None]:
        return {
            "html": MIMEType.html,
            "css": MIMEType.css,
            "js": MIMEType.js,
            "json": MIMEType.json,
            "ico": MIMEType.ico,
        }.get(extension)


class Marker(StrEnum):
    FILE = "%FILE%"


class Method(StrEnum):
    GET = "GET"
    POST = "POST"

    @staticmethod
    def all() -> tuple["Method", ...]:
        return (Method.GET, Method.POST)


class Header(StrEnum):
    Connection = "Connection"

    class ConnectionV(StrEnum):
        KeepAlive = "keep-alive"

    ContentType = "Content-Type"
    ContentLength = "Content-Length"
    TransferEncoding = "Transfer-Encoding"

    class TransferEncodingV(StrEnum):
        Chunked = "chunked"


class Code(StrEnum):
    i100 = "Continue"
    i101 = "Switching Protocols"
    i103 = "Early Hints"
    s200 = "OK"
    s201 = "Created"
    s202 = "Accepted"
    s203 = "Non-Authoritative Information"
    s204 = "No Content"
    s205 = "Reset Content"
    s206 = "Partial Content"
    r300 = "Multiple Choices"
    r301 = "Moved Permanently"
    r302 = "Found"
    r303 = "See Other"
    r304 = "Not Modified"
    r307 = "Temporary Redirect"
    r308 = "Permanent Redirect"
    e400 = "Bad Request"
    e401 = "Unauthorized"
    e402 = "Payment Required"
    e403 = "Forbidden"
    e404 = "Not Found"
    e405 = "Method Not Allowed"
    e406 = "Not Acceptable"
    e407 = "Proxy Authentication Required"
    e408 = "Request Timeout"
    e409 = "Conflict"
    e410 = "Gone"
    e411 = "Length Required"
    e412 = "Precondition Failed"
    e413 = "Payload Too Large"
    e414 = "URI Too Long"
    e415 = "Unsupported Media Type"
    e416 = "Range Not Satisfiable"
    e417 = "Expectation Failed"
    e418 = "I'm a teapot"
    e422 = "Unprocessable Entity"
    e425 = "Too Early"
    e426 = "Upgrade Required"
    e428 = "Precondition Required"
    e429 = "Too Many Requests"
    e431 = "Request Header Fields Too Large"
    e451 = "Unavailable For Legal Reasons"
    e500 = "Internal Server Error"
    e501 = "Not Implemented"
    e502 = "Bad Gateway"
    e503 = "Service Unavailable"
    e504 = "Gateway Timeout"
    e505 = "HTTP Version Not Supported"
    e506 = "Variant Also Negotiates"
    e507 = "Insufficient Storage"
    e508 = "Loop Detected"
    e510 = "Not Extended"
    e511 = "Network Authentication Required"

    @staticmethod
    def get_value(code: "Code") -> int:
        return {
            Code.i100: 100,
            Code.i101: 101,
            Code.i103: 103,
            Code.s200: 200,
            Code.s201: 201,
            Code.s202: 202,
            Code.s203: 203,
            Code.s204: 204,
            Code.s205: 205,
            Code.s206: 206,
            Code.r300: 300,
            Code.r301: 301,
            Code.r302: 302,
            Code.r303: 303,
            Code.r304: 304,
            Code.r307: 307,
            Code.r308: 308,
            Code.e400: 400,
            Code.e401: 401,
            Code.e402: 402,
            Code.e403: 403,
            Code.e404: 404,
            Code.e405: 405,
            Code.e406: 406,
            Code.e407: 407,
            Code.e408: 408,
            Code.e409: 409,
            Code.e410: 410,
            Code.e411: 411,
            Code.e412: 412,
            Code.e413: 413,
            Code.e414: 414,
            Code.e415: 415,
            Code.e416: 416,
            Code.e417: 417,
            Code.e418: 418,
            Code.e422: 422,
            Code.e425: 425,
            Code.e426: 426,
            Code.e428: 428,
            Code.e429: 429,
            Code.e431: 431,
            Code.e451: 451,
            Code.e500: 500,
            Code.e501: 501,
            Code.e502: 502,
            Code.e503: 503,
            Code.e504: 504,
            Code.e505: 505,
            Code.e506: 506,
            Code.e507: 507,
            Code.e508: 508,
            Code.e510: 510,
            Code.e511: 511,
        }[code]
