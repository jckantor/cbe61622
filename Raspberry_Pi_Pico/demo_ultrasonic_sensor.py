# Seeed Grove Ultrasonic Sensor v2
#
# https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/
# #play-with-raspberry-pi-with-grove-base-hat-for-raspberry-pi

import machine
import utime

# blink on-board led to verify operating status

led = machine.Pin(25, machine.Pin.OUT)
def blink(timer):
    global led
    led.toggle()
    
machine.Timer(freq=2, mode=machine.Timer.PERIODIC, callback=blink)


def get_distance(gpio):
    
    # send pulse
    gpio.init(machine.Pin.OUT)
    gpio.value(0)
    utime.sleep_us(2)
    gpio.value(1)
    utime.sleep_us(10)
    gpio.value(0)
    
    # listen for response
    gpio.init(machine.Pin.IN)
    
    # wait for on
    t0 = utime.ticks_us()
    count = 0
    while count < 10000:
        if gpio.value():
            break
        count += 1
        
    # wait for off
    t1 = utime.ticks_us()
    count = 0
    while count < 10000:
        if not gpio.value():
            break
        count += 1
    
    t2 = utime.ticks_us()
    
    if t1 - t2 > 530:
        return None
    else:
        return (t2 - t1) / 29 / 2
    
    
sensor = machine.Pin(27)

def report_distance(timer):
    global sensor
    d = get_distance(sensor)
    print(d)


machine.Timer(freq=10, mode=machine.Timer.PERIODIC, callback=report_distance)
