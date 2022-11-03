%serialconnect

from machine import Pin, PWM
import time

class Servo(object):
    def __init__(self, gpio, freq=50):
        self.gpio = gpio
        self.pwm = PWM(Pin(gpio, Pin.IN))
        self.pwm.freq(freq)
        self.pwm.duty_ns(0)
        
    def set_value(self, value):
        self.pulse_us = 500 + 20*max(0, min(100, value))
        self.pwm.duty_ns(int(1000*self.pulse_us))
        
    def off(self):
        self.pwm.duty_ns(0)
        

servo = Servo(16)

servo.set_value(0)
time.sleep(2)
servo.set_value(100)
time.sleep(2)
    
servo.off()

from machine import Pin, I2C
from lcd1602 import LCD1602 as LCD


class Screen(object):
    def __init__(self, id, sda, scl):
        self.sda = Pin(sda, Pin.OUT)
        self.scl = Pin(scl, Pin.OUT)
        self.i2c = I2C(id, sda=self.sda, scl=self.scl)
        self.lcd = LCD(self.i2c, 2, 16)
        self.lcd.clear()
        
    def print(self, lines):
        for k, line in enumerate(lines):
            if line is not None:
                self.lcd.setCursor(0, k)
                self.lcd.print(line)
        
        
screen0 = Screen(0, sda=8, scl=9)
screen1 = Screen(1, sda=6, scl=7)
        
screen0.print(("Hello World", "Go Irish!"))
screen1.print(["", "Hello"])


from machine import Pin

class PWM_motor(object):
    def __init__(self, gpio):
        self.pwm = PWM(Pin(gpio))
           
class Servo(PWM_motor):
    def __init__(self, gpio, freq=50):
        super(Y, self).__init__(gpio)
        self.pwm.freq(freq)
        
    def set_value(self, value):
        self.pulse_us = 500 + 20*max(0, min(100, value))
        self.pwm.duty_ns(int(1000*self.pulse_us))
        
servo = Servo(16)
servo.set_value(50)

import machine
import time

class UltrasonicSensor(object):
    def __init__(self, gpio):
        self.pin = Pin(gpio)
        
    def get_distance_cm(self):
        # send pulse
        self.pin.init(Pin.OUT)
        self.pin.value(0)
        time.sleep_us(2)
        self.pin.value(1)
        time.sleep_us(10)
        self.pin.value(0)

        # listen for response
        self.pin.init(Pin.IN)

        # wait for on
        t0 = time.ticks_us()
        count = 0
        while count < 10000:
            if self.pin.value():
                break
            count += 1

        # wait for off
        t1 = time.ticks_us()
        count = 0
        while count < 10000:
            if not self.pin.value():
                break
            count += 1

        t2 = time.ticks_us()

        if t1 - t2 < 530:
            return (t2 - t1) / 29 / 2
        else:
            return 0
        
sensor = UltrasonicSensor(20)
print(sensor.get_distance_cm())

from machine import Pin, I2C, ADC, PWM
import time
from lcd1602 import LCD1602 as LCD
from knob import Knob


class Servo(object):
    def __init__(self, gpio, freq=50):
        self.gpio = gpio
        self.pwm = PWM(Pin(gpio))
        self.pwm.freq(freq)
        self.pwm.duty_ns(0)
        
    def set_value(self, value):
        self.pulse_us = 500 + 20*max(0, min(100, value))
        self.pwm.duty_ns(int(1000*self.pulse_us))
        
    def off(self):
        self.pwm.duty_ns(0)


class Screen(object):
    def __init__(self, id, sda, scl):
        self.sda = Pin(sda, Pin.OUT)
        self.scl = Pin(scl, Pin.OUT)
        self.i2c = I2C(id, sda=self.sda, scl=self.scl)
        self.lcd = LCD(self.i2c, 2, 16)
        self.lcd.clear()
        
    def print(self, lines):
        for k, line in enumerate(lines):
            if line is not None:
                self.lcd.setCursor(0, k)
                self.lcd.print(line)


## set up led
led = Pin(25, Pin.OUT)

## set up lcd display 0
display0 = Screen(0, sda=8, scl=9)
display1 = Screen(1, sda=6, scl=7)

## setup rotary angle sensors
knob0 = Knob(26)
knob1 = Knob(27)

## setup ultra-sonic distance sensor on Pin 20
sensor = UltrasonicSensor(20)

## set up servo motor
servo = Servo(16)

start = time.time()
ball_position = 0

while time.time() - start < 20:

    ball_position = sensor.get_distance_cm()
    ball_setpoint = 50*knob0.get_value()/100
    display0.print([f"SP = {ball_setpoint:0.2f} cm", 
                f"PV = {ball_position:0.2f} cm"])
    
    Kp = knob1.get_value()
    u = Kp*(ball_setpoint - ball_position)
    servo.set_value(u)
    
    display1.print([f"Kp = {Kp}", f"MV = {dt_us}"])
    time.sleep(0.1)

servo.off()
