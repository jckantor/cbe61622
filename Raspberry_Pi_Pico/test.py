import machine
import utime


gp00 = machine.Pin(0, machine.Pin.OUT)
while True:
    gp00.toggle()
    utime.sleep(0.001)