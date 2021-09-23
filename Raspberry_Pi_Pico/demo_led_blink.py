import machine
import utime


led = machine.Pin(25, machine.Pin.OUT)
gp0 = machine.Pin(0, machine.Pin.OUT)

def blink_led(timer):
    global led
    led.toggle()
    
def blink_gp0(timer):
    global gp0
    gp0.toggle()
    
machine.Timer(freq=5, mode=machine.Timer.PERIODIC, callback=blink_led)
machine.Timer(freq=1, mode=machine.Timer.PERIODIC, callback=blink_gp0)
