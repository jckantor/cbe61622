# Seeed Grove Ultrasonic Sensor v2
#
# https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
# #play-with-raspberry-pi-with-grove-base-hat-for-raspberry-pi

import machine
import time

# blink on-board led to verify operating status

led = machine.Pin(25, machine.Pin.OUT)
def blink(timer):
    global led
    led.toggle()
    
machine.Timer(freq=2, mode=machine.Timer.PERIODIC, callback=blink)


def get_distance(pin):
    
    # send pulse
    pin.init(machine.Pin.OUT)
    pin.value(0)
    time.sleep_us(2)
    pin.value(1)
    time.sleep_us(10)
    pin.value(0)
    
    # listen for response
    pin.init(machine.Pin.IN)
    
    # wait for on
    t0 = time.ticks_us()
    count = 0
    while count < 10000:
        if pin.value():
            break
        count += 1
        
    # wait for off
    t1 = time.ticks_us()
    count = 0
    while count < 10000:
        if not pin.value():
            break
        count += 1
    
    t2 = time.ticks_us()
    
    if t1 - t2 > 530:
        return None
    else:
        return (t2 - t1) / 29 / 2
    
    
sensor = machine.Pin(20)

def report_distance(timer):
    global sensor
    d = get_distance(sensor)
    print(d)


machine.Timer(freq=10, mode=machine.Timer.PERIODIC, callback=report_distance)
