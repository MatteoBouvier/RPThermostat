# pyright: reportImplicitRelativeImport=false
import json

import config
from udatetime import datetime
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
    with open("data.json") as file:
        data = json.load(file)

    return parse(
        "html/index.html",
        temp=dict(current=data["temp"]["current"], **data["config"]["minmax"]),
        time=data["config"]["days"],
        weekdays=[
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche",
        ],
    )


@app.get("/api/status", MIMEType.json)
def api_get_status() -> str:
    with open("data.json") as file:
        data = json.load(file)

    return json.dumps({"active": data["active"]})


@app.post("/api/status", MIMEType.json)
def api_post_status(request: Request) -> str:
    with open("data.json") as file:
        data = json.load(file)

    set_active = request.json().get("active")

    if set_active is not None:
        data["active"] = bool(set_active)
        with open("data.json", "w") as file:
            json.dump(data, file)

        return json.dumps({"active": bool(set_active)})

    else:
        return json.dumps({})


@app.get("/api/days", MIMEType.json)
def api_get_days() -> str:
    with open("data.json") as file:
        data = json.load(file)

    return json.dumps(data["config"]["days"])


@app.get("/api/days/{day}", MIMEType.json)
def api_get_day(day: str) -> str:
    with open("data.json") as file:
        data = json.load(file)

    return json.dumps(data["config"]["days"][day])


@app.get("/api/temp", MIMEType.json)
def api_get_temp() -> str:
    with open("data.json") as file:
        data = json.load(file)

    now = datetime.now()
    weekday = now.strftime("%A")

    start, end = data["config"]["days"][weekday]
    extras = dict(current=data["temp"]["current"], rising=data["temp"]["rising"])

    if start * 60 > now.hour * 60 + now.minute > end * 60:
        return json.dumps(data["config"]["minmax"]["day"] | extras)

    else:
        return json.dumps(data["config"]["minmax"]["night"] | extras)


@app.post("/api/temp", MIMEType.json)
def api_post_temp(request: Request) -> str:
    modifications: dict[str, dict[str, float]] = {}
    for time, d in request.json().items():
        for ex, value in d.items():
            print("set", time, ex, value)

            modifications.setdefault(time, {})[ex] = value

    return json.dumps(modifications)


app.run()
