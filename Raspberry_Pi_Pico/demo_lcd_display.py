# Grove-LCD RGB Backlight V4.0

import machine

sda = machine.Pin(0)
scl = machine.Pin(1)
i2c = machine.I2C(0, sda=sda, scl=scl, freq=400000)

print(i2c.scan())

TXT_ADDR = 0x3e  # decimal 62
RGB_ADDR = 0x62  # decimal 98
XXX_ADDR = 0x70  # decimal 112

i2c.writeto_mem(RGB_ADDR, 0, 0x00)