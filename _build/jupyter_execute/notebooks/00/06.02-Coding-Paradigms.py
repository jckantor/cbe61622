%serialconnect

from machine import Pin, ADC
import time

        


from machine import Pin, I2C, ADC, PWM
import time
from lcd1602 import LCD1602 as LCD

class Knob(object):
    def __init__(self, gpio):
        self.gpio = gpio
        self.adc = ADC(Pin(gpio))
        
    def value(self):
        return 100*self.adc.read_u16()/65535


## set up led
led = Pin(25, Pin.OUT)

## set up lcd display 0
sda = Pin(8, Pin.OUT)
scl = Pin(9, Pin.OUT)
i2c0 = I2C(0, sda=sda, scl=scl)

dsp0 = LCD(i2c0, 2, 16)
dsp0.clear()
dsp0.setCursor(0, 0)
dsp0.print("Hello, World")
dsp0.setCursor(0, 1)
dsp0.print("Display 0")

## set up lcd display 1
sda = Pin(6, Pin.OUT)
scl = Pin(7, Pin.OUT)
i2c1 = I2C(1, sda=sda, scl=scl)

dsp1 = LCD(i2c1, 2, 16)
dsp1.clear()
dsp1.setCursor(0, 0)
dsp1.print("Hello, World")
dsp1.setCursor(0, 1)
dsp1.print("Display 1")

## setup rotary angle sensors
knob0 = Knob(26)
knob1 = Knob(27)

## setup ultra-sonic distance sensor on Pin 20
dst = Pin(20)

## set up servo motor
pwm = PWM(Pin(16))
pwm.freq(50)
pwm.duty_ns(1000*1500)

start = time.time()
ball_position = 0

while time.time() - start < 20:

    # read distance
    # send pulse
    dst.init(Pin.OUT)
    dst.value(0)
    time.sleep_us(2)
    dst.value(1)
    time.sleep_us(10)
    dst.value(0)
    
    # listen for response
    dst.init(Pin.IN)
    
    # wait for on
    t0 = time.ticks_us()
    count = 0
    while count < 10000:
        if dst.value():
            break
        count += 1
        
    # wait for off
    t1 = time.ticks_us()
    count = 0
    while count < 10000:
        if not dst.value():
            break
        count += 1
    
    t2 = time.ticks_us()
    
    if t1 - t2 < 530:
        ball_position = (t2 - t1) / 29 / 2
        
    # read analog sensor
    ball_setpoint = 50*knob0.value()/100
       
    # display ball state
    dsp0.clear()
    dsp0.setCursor(0, 0)
    dsp0.print(f"SP = {ball_setpoint:0.2f} cm")
    dsp0.setCursor(0, 1)
    dsp0.print(f"PV = {ball_position}")
    
    # measure control gain
    Kp = knob1.value()
    
    # update servo
    
    # adjust servo
    u = Kp*(ball_setpoint - ball_position)
    dt_us = int(1500 + max(-1000, min(1000, u)))
    pwm.duty_ns(1000*dt_us)
    
    # display controller state
    dsp1.clear()
    dsp1.setCursor(0, 0)
    dsp1.print(f"Kp = {Kp}")
    dsp1.setCursor(0, 1)
    dsp1.print(f"MV = {dt_us}")
    
    time.sleep(0.1)
    
