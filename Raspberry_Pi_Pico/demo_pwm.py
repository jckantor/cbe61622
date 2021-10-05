# demo pwm module

import machine
import utime

def light_led(intensity, duration=1):
    led = machine.Pin(25, mode=machine.Pin.OUT)
    pwm = machine.PWM(led)
    pwm.freq(1000)
    pwm.duty_u16(int(intensity*65535))
    utime.sleep(duration)
    pwm.duty_u16(0)
    pwm.deinit()

def sound_buzzer(tone, intensity):
    buzzer = machine.Pin(18, mode=machine.Pin.OUT)
    pwm = machine.PWM(buzzer)
    pwm.freq(tone)
    pwm.duty_u16(int(intensity*65535))


light_led(0.75, 2.5)
