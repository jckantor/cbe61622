# demo PWM using on-board LED

import machine
import utime

pin = machine.Pin(0, mode=machine.Pin.OUT)
while True:
    pin.toggle()
    utime.sleep_us(100)
    