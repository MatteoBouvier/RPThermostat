import onewire
import ds18x20
from machine import Pin, PWM

class Thermometer:
    def __init__(self, pin: int):
        ow = onewire.OneWire(Pin(pin))
        self.ds = ds18x20.DS18X20(ow)
        self.devices = self.ds.scan()

        if not len(self.devices):
            raise ValueError('No devices found')
        
    def get_temp(self) -> float:
        self.ds.convert_temp()
        return self.ds.read_temp(self.devices[0])