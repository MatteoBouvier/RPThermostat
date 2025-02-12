import time
from machine import Pin, PWM


class Servo:
    _SERVO_PWM_FREQ: int = 50
    _MIN_u16_DUTY: int = 1850  # offset for correction
    _MAX_u16_DUTY: int = 8300  # offset for correction
    _MIN_ANGLE: int = 0
    _MAX_ANGLE: int = 180

    _angle_conversion_factor: float = (_MAX_u16_DUTY - _MIN_u16_DUTY) / (
        _MAX_ANGLE - _MIN_ANGLE
    )

    def __init__(self, pin: int):
        self._current_angle: float = -1.0
        self._pin: int = pin

        self._motor: PWM = PWM(Pin(pin))
        self._motor.freq(Servo._SERVO_PWM_FREQ)

    @staticmethod
    def angle_to_u16_duty(angle: float) -> int:
        return (
            int((angle - Servo._MIN_ANGLE) * Servo._angle_conversion_factor)
            + Servo._MIN_u16_DUTY
        )

    def __repr__(self) -> str:
        return "Servo(pin={0}, angle={1})".format(self._pin, self._current_angle)

    def rotate(self, *angles: float) -> None:
        for angle in angles:
            angle = round(angle, 2)

            if angle == self._current_angle:
                continue

            _ = self._motor.duty_u16(Servo.angle_to_u16_duty(angle))
            self._current_angle = angle

            time.sleep(0.5)
