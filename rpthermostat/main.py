# pyright: reportImplicitRelativeImport=false
import json


import config
from server import Nice, MIMEType
from server.utils import connect_wifi
from template import parse

MICROPYTHON = False

if MICROPYTHON:
    connect_wifi(config.SSID, config.PASSWORD)
    app = Nice(source_folder="html")

else:
    app = Nice(port=8080, source_folder="html", use_micro_python=False)


@app.route("/")
def index() -> str:
    return parse(
        "html/index.html",
        temp=dict(current=17.2, day=dict(min=16, max=19), night=dict(min=15, max=17)),
    )


@app.route("/api/temp", MIMEType.json)
def api_get_temp() -> str:
    return json.dumps({"min": 16, "max": 19, "current": 17.2})


app.run()
