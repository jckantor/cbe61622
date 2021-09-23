import machine
import utime

pins = [machine.Pin(i, machine.Pin.OUT) for i in range(16)]

for k in range(20):
    for p in pins:
        p.toggle()
        utime.sleep_ms(10)
