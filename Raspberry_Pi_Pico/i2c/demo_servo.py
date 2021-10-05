import machine
import time

servo_pin = machine.Pin(7, mode=machine.Pin.OUT)
servo_pwm = machine.PWM(servo_pin)
servo_pwm.freq(50)

# pulse width ranges from 500 to 1500 microseconds

class Servo():
    
    def __init__(self, gpio, freq=50, pw_min=500, pw_max=2200):
        self.pin = machine.Pin(gpio, mode=machine.Pin.OUT)
        self.pw_min = pw_min
        self.pw_max = pw_max
        self.pwm = machine.PWM(self.pin)
        self.pwm.freq(freq)
        
    def set_position(self, pos):
        pw = self.pw_min + int((self.pw_max - self.pw_min)*pos/100)
        self.set_pulsewidth_us(max(self.pw_min, min(self.pw_max, pw)))
        
    def set_pulsewidth_us(self, pw):
        self.pwm.duty_ns(1000*pw)
                         

srv = Servo(7)
srv.set_position(0)
time.sleep(1)
for k in range(0, 101):
    srv.set_position(k)
    time.sleep_ms(20)