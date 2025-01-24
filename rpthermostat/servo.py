from time import sleep
from machine import Pin, PWM

class Servo:
    _SERVO_PWM_FREQ = 50
    _MIN_u16_DUTY = 1720 # offset for correction
    _MAX_u16_DUTY = 8400  # offset for correction
    _MIN_ANGLE = 0
    _MAX_ANGLE = 180
    
    _angle_conversion_factor = (_MAX_u16_DUTY - _MIN_u16_DUTY) / (_MAX_ANGLE - _MIN_ANGLE)
        
    
    @staticmethod
    def angle_to_u16_duty(angle: float) -> int:       
        return int((angle - Servo._MIN_ANGLE) * Servo._angle_conversion_factor) + Servo._MIN_u16_DUTY


    def __init__(self, pin: int):
        self.current_angle = -1
        self._pin = pin
        
        self._motor = PWM(Pin(pin))
        self._motor.freq(Servo._SERVO_PWM_FREQ)
        
        self.rotate(0.0)
        
    def __repr__(self) -> str:
        return f"Servo(pin={self._pin}, angle={self.current_angle})"


    def rotate(self, *angles: list[float]) -> None:
        for angle in angles:
            angle = round(angle, 2)
        
            if angle == self.current_angle:
                continue
        
            self._motor.duty_u16(Servo.angle_to_u16_duty(angle))
            self.current_angle = angle
            
            sleep(1)
            print('rotated to', angle)
            