import machine
import utime

# blink on-board led

led_onboard = machine.Pin(25, machine.Pin.OUT)
for k in range(10):
    led_onboard.toggle()
    utime.sleep(0.2)
    

# control brightness with PWM
led_pwm = machine.PWM(led_onboard)
led_pwm.freq(1000)
for duty in range(65025):
    led_pwm.duty_u16(duty)
    utime.sleep(0.0001)
for duty in range(65025, 0, -1):
    led_pwm.duty_u16(duty)
    utime.sleep(0.0001)
    
# buttons on GP20, GP21, GP22


led = machine.Pin(15, machine.Pin.OUT)
td = 0.01

gpio_pins = [machine.Pin(k, machine.Pin.OUT) for k in range(0, 16)]

while True:
    for pin in gpio_pins:
        pin.value(1)
        utime.sleep(td)
    for pin in gpio_pins:
        pin.value(0)
        utime.sleep(td)
        







    #led.value(1)
    #utime.sleep(1)
    #led.value(0)
    #utime.sleep(1)
    