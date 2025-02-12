import json
import asyncio
import machine

from config import TYPE_CHECKING
from servo import Servo
from thermometer import Thermometer
from udatetime import datetime

if TYPE_CHECKING:
    from typing import Any
    from enum import StrEnum

else:
    StrEnum = object


class State(StrEnum):
    OFF = "OFF"
    IDLE = "IDLE"
    RISING = "RISING"

    @staticmethod
    def should_click(current_state: "State", new_state: "State") -> bool:
        return {
            State.OFF: {State.IDLE: False, State.RISING: True},
            State.IDLE: {
                State.OFF: False,
                State.RISING: True,
            },
            State.RISING: {
                State.OFF: True,
                State.IDLE: True,
            },
        }[current_state][new_state]


class Thermostat:
    _servo_Pin: int = 0
    _DS18B20_Pin: int = 22

    def __init__(self, period: float = 10.0):
        self.period: float = period
        self._control_task: asyncio.Task[Any] | None = None
        self._led_task: asyncio.Task[Any] | None = None

        self.state: State = State.OFF

        self.led: machine.Pin = machine.Pin("LED", machine.Pin.OUT)
        self.servo: Servo = Servo(Thermostat._servo_Pin)
        self.thermometer: Thermometer = Thermometer(Thermostat._DS18B20_Pin)

        self.servo.rotate(180)

        with open("data.json", "r") as file:
            self.config: dict[str, Any] = json.load(file)

    @property
    def is_active(self) -> bool:
        return self.state != State.OFF

    @property
    def is_rising(self) -> bool:
        return self.state == State.RISING

    @property
    def min_max_temp(self) -> tuple[float, float]:
        now = datetime.now()
        weekday = now.strftime("%A")

        start, end = self.config["days"][weekday]

        if start * 60 < now.hour * 60 + now.minute < end * 60:
            minmax = self.config["minmax"]["day"]
            return minmax["min"], minmax["max"]

        else:
            minmax = self.config["minmax"]["night"]
            return minmax["min"], minmax["max"]

    def update(
        self, what: dict[str, Any], config: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        modifications: dict[str, Any] = {}

        if config is None:
            config = self.config

        for key, value in what.items():
            if isinstance(value, dict):
                modifications[key] = self.update(value, config[key])

            else:
                value = (
                    [float(e) for e in value]
                    if isinstance(value, list)
                    else float(value)
                )
                config[key] = value
                modifications[key] = value

        with open("data.json", "w") as file:
            json.dump(self.config, file)

        return modifications

    def click(self) -> None:
        self.servo.rotate(0, 180)

    def _update_state(self, state: State) -> None:
        if self.state == state:
            return

        if State.should_click(self.state, state):
            self.click()

        if state == State.OFF:
            print("turning OFF")

        elif state == State.IDLE:
            print("rising -> idle")

            if self._led_task is not None:
                _ = self._led_task.cancel()

            loop = asyncio.get_event_loop()
            self._led_task = loop.create_task(self._blink_slow())

        elif state == State.RISING:
            print("idle -> rising")

            if self._led_task is not None:
                _ = self._led_task.cancel()

            loop = asyncio.get_event_loop()
            self._led_task = loop.create_task(self._blink_fast())

        self.state = state

    async def _control(self) -> None:
        while True:
            temperature = self.thermometer.get_temp()
            min_temp, max_temp = self.min_max_temp

            if self.state == State.IDLE and temperature < min_temp:
                print(temperature, ">>", max_temp)
                self._update_state(State.RISING)

            elif self.state == State.RISING and temperature > max_temp:
                print(temperature, "<<", min_temp)
                self._update_state(State.IDLE)

            else:
                print(temperature, "keep [{0} -> {1}]".format(min_temp, max_temp))

            await asyncio.sleep(60 * self.period)

    async def _blink_slow(self) -> None:
        while True:
            self.led.toggle()

            await asyncio.sleep(2)

    async def _blink_fast(self) -> None:
        while True:
            self.led.toggle()

            await asyncio.sleep(0.5)

    def run(self) -> None:
        loop = asyncio.get_event_loop()
        self._control_task = loop.create_task(self._control())
        self._led_task = loop.create_task(self._blink_slow())

        self._update_state(State.IDLE)

    def stop(self) -> None:
        if self._control_task is not None:
            _ = self._control_task.cancel()
            self._control_task = None

        if self._led_task is not None:
            _ = self._led_task.cancel()
            self._led_task = None

        self._update_state(State.OFF)


# TODO:
# log temp to file
