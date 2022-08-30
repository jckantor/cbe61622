%serialconnect

import machine
import time

led = machine.Pin(25, machine.Pin.OUT)
start = time.time()
while time.time() - start <= 20:
    led.toggle()
    time.sleep_ms(500)


