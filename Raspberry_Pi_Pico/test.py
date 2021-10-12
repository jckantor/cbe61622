from machine import Pin, I2C, ADC, PWM
import time
from lcd1602 import LCD1602 as LCD

# specify i2c
sda = Pin(8, Pin.OUT)
scl = Pin(9, Pin.OUT)
i2c = I2C(0, sda=sda, scl=scl)

# create instance of display with lines and columns
dsp = LCD(i2c, 2, 16)
dsp.clear()

# Welcome display
dsp.setCursor(0, 0)
dsp.print("Hello, World")
dsp.setCursor(0, 1)
dsp.print("GO IRISH!")


