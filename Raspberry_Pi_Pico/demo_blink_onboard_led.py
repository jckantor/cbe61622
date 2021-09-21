import machine
import time

# on board led is GPIO pin 25
led = machine.Pin(25, machine.Pin.OUT)

# toggle led on and off until reset
while True:
    led.toggle()
    time.sleep(0.5)