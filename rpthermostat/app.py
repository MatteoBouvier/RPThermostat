import json

import _secrets
from udatetime import datetime
from miniwebserver import WebServer, MIMEType, Request
from miniwebserver.template import parse
from thermostat import Thermostat
from wifi import connect_wifi

with open("data.json") as file:
    data = json.load(file)

thermostat = Thermostat(period=0.05)

connect_wifi(_secrets.SSID, _secrets.PASSWORD)
app = WebServer(source_folder="html", thermostat=thermostat)


@app.get("/")
def index() -> str:
    thermostat: Thermostat = app.globals["thermostat"]

    return parse(
        "html/index.html",
        temp=dict(
            current=thermostat.thermometer.get_temp(), **thermostat.config["minmax"]
        ),
        time=thermostat.config["days"],
        weekdays=[
            "Lundi",
            "Mardi",
            "Mercredi",
            "Jeudi",
            "Vendredi",
            "Samedi",
            "Dimanche",
        ],
        now=datetime.now(),
    )


@app.get("/api/status", MIMEType.json)
def api_get_status() -> str:
    thermostat: Thermostat = app.globals["thermostat"]

    return json.dumps({"active": thermostat.is_active})


@app.post("/api/status", MIMEType.json)
def api_post_status(request: Request) -> str:
    thermostat: Thermostat = app.globals["thermostat"]
    set_active = request.json().get("active")

    if set_active is not None:
        if set_active and not thermostat.is_active:
            thermostat.run()

        elif not set_active and thermostat.is_active:
            thermostat.stop()

        return json.dumps({"active": thermostat.is_active})

    else:
        return json.dumps({})


@app.get("/api/days", MIMEType.json)
def api_get_days() -> str:
    thermostat: Thermostat = app.globals["thermostat"]
    return json.dumps(thermostat.config["days"])


@app.get("/api/days/{day}", MIMEType.json)
def api_get_day(day: str) -> str:
    thermostat: Thermostat = app.globals["thermostat"]
    return json.dumps(thermostat.config["days"][day])


@app.get("/api/temp", MIMEType.json)
def api_get_temp() -> str:
    thermostat: Thermostat = app.globals["thermostat"]

    min_, max_ = thermostat.min_max_temp
    return json.dumps(
        dict(
            current=round(float(thermostat.thermometer.get_temp()), 1),
            rising=thermostat.is_rising,
            min=min_,
            max=max_,
        )
    )


@app.get("/api/temp/{time}", MIMEType.json)
def api_get_temp_time(time: str) -> str:
    thermostat: Thermostat = app.globals["thermostat"]

    return json.dumps(thermostat.config["minmax"][time])


@app.post("/api/temp", MIMEType.json)
def api_post_temp(request: Request) -> str:
    thermostat: Thermostat = app.globals["thermostat"]

    modifications = thermostat.update(request.json())
    return json.dumps(modifications)
