import machine
from lcd1602 import LCD1602_RGB

# specify i2c
sda = machine.Pin(8, machine.Pin.OUT)
scl = machine.Pin(9, machine.Pin.OUT)
i2c = machine.I2C(0, sda=sda, scl=scl)

# create instance of display with lines and columns
d = LCD1602_RGB(i2c, 2, 16)
d.clear()
d.set_rgb(10, 10, 20)
d.display()
d.blink()
d.cursor()

# Welcome display
d.setCursor(0, 0)
d.write(ord("A"))
d.print("Hello, World")
d.setCursor(0, 1)
d.print("GO IRISH!")