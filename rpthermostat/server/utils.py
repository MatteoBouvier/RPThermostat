import io
import sys
import time

from .http.utils import html_document

try:
    import network  # pyright: ignore[reportMissingImports]
except ImportError:
    pass

try:
    import traceback
except ImportError:
    pass


def connect_wifi(ssid: str, password: str, timeout: int | None = 30) -> None:
    """Attempt connecting to the wifi using SSID and password.
    Raises an OSError if connection could not be established after `timeout` seconds, if timeout is not set to None."""
    sta_if = network.WLAN(network.WLAN.IF_STA)  # pyright: ignore[reportPossiblyUnboundVariable, reportUnknownMemberType, reportUnknownVariableType]
    sta_if.active(True)  # pyright: ignore[reportUnknownMemberType]
    sta_if.connect(ssid, password)  # pyright: ignore[reportUnknownMemberType]

    start = time.time()
    while not sta_if.isconnected():  # pyright: ignore[reportUnknownMemberType]
        if timeout is not None and (time.time() - start) > timeout:
            raise OSError("Could not connect to Wifi")

    print("Connected to Wifi")
    print("Using IP address", sta_if.ifconfig()[0])  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]


def print_exception(err: Exception) -> str:
    """Print exception to stderr AND return traceback formatted to HTML"""
    print("[Warning] An internal error occured:", file=sys.stderr)

    if hasattr(sys, "print_exception"):
        err_str_buffer = io.StringIO()
        sys.print_exception(err, err_str_buffer)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType]
        err_str = err_str_buffer.getvalue()

    else:
        err_str = "".join(traceback.format_exception(err))  # pyright: ignore[reportPossiblyUnboundVariable]
        print(err_str, file=sys.stderr)

    return html_document(
        "500 Internal Server Error",
        head="""<style>
body {
  padding: 1rem 4rem;
}

</style>""",
        body=f"""<h1>Internal Server Error</h1>
<div style="background: #F6C479; border: 1px solid #232326; border-radius: .5rem; padding: 1rem;">
  {err_str.replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")}
</div>""",
    )
