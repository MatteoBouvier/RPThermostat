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
        
        self.servo = PWM(Pin(Thermostat._servo_Pin))
        self.servo.freq(50)
        
        ow = onewire.OneWire(Pin(Thermostat._DS18B20_Pin))
        self.ds = ds18x20.DS18X20(ow)
        self.devices = self.ds.scan()

        if not len(self.devices):
            raise ValueError('No devices found')

        self.ds.convert_temp()
        
    def get_temp(self) -> float:
        return self.ds.read_temp(self.devices[0])
        
    def click(self) -> None:
        self.servo.duty_ns(0)
        time.sleep(1)
        self.servo.duty_u16(1277)
        time.sleep(0.38)
        self.servo.duty_u16(5277)
        time.sleep(0.37)
        self.servo.duty_ns(0)
        
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
            temperature = self.get_temp()
            print(temperature, self._min_temp)
            
            if self.state == "IDLE" and temperature < self._min_temp:
                self._update_state("RISING_TEMP")
                
            elif self.state == "RISING_TEMP" and temperature > self._max_temp:
                self._update_state("IDLE")
                
            else:
                print('keep')
            
        self.timer.init(period=int(1000 * 60 * period), callback=callback)
        
        

Thermostat(30, 40).run()








