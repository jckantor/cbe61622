from machine import Pin, ADC

class Knob(object):
    def __init__(self, gpio):
        self.gpio = gpio
        self.adc = ADC(Pin(gpio))
        
    def get_value(self):
        return 100*self.adc.read_u16()/65535