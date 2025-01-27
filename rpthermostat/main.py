# pyright: reportImplicitRelativeImport=false
import json


import config
from server import Nice, MIMEType, Request
from server.utils import connect_wifi
from template import parse

MICROPYTHON = False

if MICROPYTHON:
    connect_wifi(config.SSID, config.PASSWORD)
    app = Nice(source_folder="html")

else:
    app = Nice(port=8080, source_folder="html", use_micro_python=False)


@app.get("/")
def index() -> str:
    return parse(
        "html/index.html",
        temp=dict(current=17.2, day=dict(min=16, max=19), night=dict(min=15, max=17)),
    )


@app.get("/api/status", MIMEType.json)
def api_get_status() -> str:
    return json.dumps({"active": False})


@app.post("/api/status", MIMEType.json)
def api_post_status(request: Request) -> str:
    set_active = request.json().get("active")
    if set_active is not None:
        return json.dumps({"active": set_active})

    else:
        return json.dumps({})


@app.get("/api/temp", MIMEType.json)
def api_get_temp() -> str:
    return json.dumps({"min": 16, "max": 19, "current": 17.2})


@app.post("/api/temp", MIMEType.json)
def api_post_temp(request: Request) -> str:
    modifications: dict[str, dict[str, float]] = {}
    for time, d in request.json().items():
        for ex, value in d.items():
            print("set", time, ex, value)

            modifications.setdefault(time, {})[ex] = value

    return json.dumps(modifications)


app.run()
