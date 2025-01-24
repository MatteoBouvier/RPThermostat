# import machine
# led = machine.Pin("LED", machine.Pin.OUT)
# timer = machine.Timer()
# 
# def blink(timer):
#     led.toggle()
#     
# 
# timer.init(freq=2.5, mode=machine.Timer.PERIODIC, callback=blink)

import onewire
import time
import ds18x20
from machine import Pin, PWM

from servo import Servo
from thermometer import Thermometer


class Thermostat:
    _servo_Pin = 0
    _DS18B20_Pin = 22
    
    def __init__(self, min_temp: float = 15, max_temp: float = 19):
        self._min_temp = min_temp
        self._max_temp = max_temp
        
        self.state = "IDLE"
        self.timer = machine.Timer()
        
        self.led = machine.Pin("LED", machine.Pin.OUT)
        self.led_timer = machine.Timer()
        self.led_timer.init(freq=1, mode=machine.Timer.PERIODIC, callback=lambda _: self.led.toggle())
        
        self.servo = Servo(Thermostat._servo_Pin)
        self.thermometer = Thermometer(Thermostat._DS18B20_Pin)
        
        self.servo.rotate(180)

        
    def click(self) -> None:
        self.servo.rotate(0, 180)
        
        
    def _update_state(self, state: str) -> None:
        if self.state == state:
            return
        
        if state == "IDLE":
            print('rising -> idle')
            self.click()
            self.led_timer.init(freq=1, mode=machine.Timer.PERIODIC, callback=lambda _: self.led.toggle())
            self.state = state
            
        elif state == "RISING_TEMP":
            print('idle -> rising')
            self.click()
            self.led_timer.init(freq=10, mode=machine.Timer.PERIODIC, callback=lambda _: self.led.toggle())
            self.state = state
            
        else:
            raise RuntimeError("Unknown state " + state)
            
        
    def run(self, period: int = 10) -> None:       
        def callback(_) -> None:
            temperature = self.thermometer.get_temp()
            
            if self.state == "IDLE" and temperature < self._min_temp:
                print(temperature, ">>", self._max_temp)
                self._update_state("RISING_TEMP")
                
            elif self.state == "RISING_TEMP" and temperature > self._max_temp:
                print(temperature, ">>", self._min_temp)
                self._update_state("IDLE")
                
            else:
                print(temperature, 'keep')

        callback(0)
            
        self.timer.init(period=int(1000 * 60 * period), callback=callback)
        
        

Thermostat(16, 19).run()

# TODO:
# log temp to file
# connect to wifi
# host web page with log and controls (on/off, min/max temp)








