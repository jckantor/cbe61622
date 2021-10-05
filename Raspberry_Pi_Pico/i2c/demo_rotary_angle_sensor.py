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
            
def display_adc(timer):
    global adc, lcd
    val = 0
    for k in range(10):
        val += 10*adc.read_u16()/65535
    lcd.update(f"ADC = {val:5.1f}%", "")

adc = machine.ADC(27)

i2c = machine.I2C(0)
lcd = LCD16x2(i2c)
lcd.update("Go Irish!", "")
time.sleep(1)

timer = machine.Timer(freq=10, mode=machine.Timer.PERIODIC, callback=display_adc)

