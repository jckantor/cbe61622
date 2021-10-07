from machine import Pin, I2C, ADC, PWM
import time
from lcd1602 import LCD1602 as LCD

# specify i2c
sda = Pin(8, Pin.OUT)
scl = Pin(9, Pin.OUT)
i2c = I2C(0, sda=sda, scl=scl)

# create instance of display with lines and columns
d = LCD(i2c, 2, 16)
d.clear()

# Welcome display
d.setCursor(0, 0)
d.print("Hello, World")
d.setCursor(0, 1)
d.print("GO IRISH!")


