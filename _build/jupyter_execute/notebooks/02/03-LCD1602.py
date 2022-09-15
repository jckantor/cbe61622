%serialconnect

import machine
from lcd1602 import LCD1602

# specify i2c
sda = machine.Pin(8, machine.Pin.OUT)
scl = machine.Pin(9, machine.Pin.OUT)
i2c = machine.I2C(0)

# create instance of display with lines and columns
d = LCD1602(i2c, 2, 16)
d.clear()

# Welcome display
d.setCursor(0, 0)
d.print("Hello, World")
d.setCursor(0, 1)
d.print("GO IRISH!")

import machine
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

# specify i2c
sda = machine.Pin(8, machine.Pin.OUT)
scl = machine.Pin(9, machine.Pin.OUT)
i2c = machine.I2C(0, sda=sda, scl=scl)

# create lcd instance
lcd = LCD16x2(i2c)
lcd.update("Hello","World")

import machine
import time

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

# set Rp2 real time clock
machine.RTC().datetime((2022, 8, 30, 0, 16, 25, 0, 0))

# Clock display
month = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
         7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

def display_date_time(timer):
    global lcd
    yr, mo, dy, h, m, s, __, __ = time.localtime()
    lcd.update(f"{dy:02d} {month[mo]} {yr}", f"{h:02d}:{m:02d}:{s:02d}")
    
# specify i2c
sda = machine.Pin(8, machine.Pin.OUT)
scl = machine.Pin(9, machine.Pin.OUT)
i2c = machine.I2C(0, sda=sda, scl=scl)

# create lcd instance
lcd = LCD16x2(i2c)

# update using Timer
timer = machine.Timer(freq=10, mode=machine.Timer.PERIODIC, callback=display_date_time)


