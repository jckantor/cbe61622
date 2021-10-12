from machine import Pin, PWM

class PWM_motor(object):
    def __init__(self, gpio):
        self.gpio = gpio
        self.pwm = PWM(Pin(gpio))
        self.value = 0
        
    def __str__(self):
        return f"{self.gpio} at {self.value}%"
        
           
class Servo(PWM_motor):
    def __init__(self, gpio, freq=50):
        super(Servo, self).__init__(gpio)
        self.pwm.freq(freq)
        
    def set_value(self, value):
        self.value = value
        self.pulse_us = 500 + 20*max(0, min(100, value))
        self.pwm.duty_ns(int(1000*self.pulse_us))
        
class Toy(PWM_motor):
    def __init__(self, gpio, freq=100):
        super(Toy, self).__init__(gpio)
        self.pwm.freq(freq)
        
    def set_value(self, value):
        self.value = value
        d = int(value*65535/100)
        self.pwm.duty_u16(d)
        
servo = Servo(16)
servo.set_value(50)

toy = Toy(18)
toy.set_value(0)

print(toy)
print(servo)