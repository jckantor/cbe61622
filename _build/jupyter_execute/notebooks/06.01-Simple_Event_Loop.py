%serialconnect

# rotary angle sensor

import machine
import time
from lcd1602 import LCD1602


class LCD16x2():
    def __init__(self, i2c):
        self.i2c = i2c
        self.d = LCD1602(i2c, 2, 16)
        self.d.clear()
        self.lines = [" "*16, " "*16]
        
    def update(self, line1=None, line2=None):
        self.update_line(0, line1)
        self.update_line(1, line2)
        
    def update_line(self, j, line):
        line = "{:16s}".format(line)
        if line != self.lines[j]:
            for i, char in enumerate(line):
                self.d.setCursor(i, j)
                self.d.write(ord(char))
            self.lines[j] = line
            
            
class RotaryAngleSensor():
    def __init__(self, adc):
        self.adc = adc
        
    def value(self, n=10):
        return (100/n/65535)*sum([self.adc.read_u16() for k in range(n)])
    

class Servo():
    def __init__(self, pwm, freq=50, pulse_width_min=500, pulse_width_max=2500):
        self.pwm = pwm
        self.pwm.freq(freq)
        self.pulse_width_min = pulse_width_min
        self.pulse_width_max = pulse_width_max
        self.pulse_width_us = 1500

    def set_position(self, pos):
        pw = self.pulse_width_min + int((self.pulse_width_max - self.pulse_width_min)*pos/100)
        self.pulse_width_us = max(self.pulse_width_min, min(self.pulse_width_max, pw))
        self.pwm.duty_ns(1000*self.pulse_width_us)
    

sensor = RotaryAngleSensor(machine.ADC(0))
lcd = LCD16x2(machine.I2C(0))
servo = Servo(machine.PWM(machine.Pin(16, machine.Pin.OUT)))

def main(timer):
    global sensor, lcd, servo
    pos = sensor.value()
    servo.set_position(pos)
    lcd.update(f"ADC = {sensor.value():5.1f}%", f"pulse = {servo.pulse_width_us} us")

timer = machine.Timer(freq=100, mode=machine.Timer.PERIODIC, callback=main)



