%serialconnect

%serialconnect

from machine import Pin
import time

btn = Pin(20, Pin.IN)

start = time.time()
while time.time() - start <= 20:
    print(btn.value(), end="")
    time.sleep(1)

%serialconnect

from machine import Pin, Timer
import time

btn = Pin(20, Pin.IN)

def check_btn(timer):
    global btn
    print(btn.value(), end="")

start = time.time()
tim = Timer(freq=1, mode=Timer.PERIODIC, callback=check_btn)

time.sleep(20)
tim.deinit()

from machine import Pin, Timer
import time

btn1 = Pin(20, Pin.IN)
btn2 = Pin(21, Pin.IN)
btn3 = Pin(22, Pin.IN)

def check_btn1(timer):
    global btn1
    print(f"btn1 = {btn1.value()}")
    
def check_btn2(timer):
    global btn2
    print(f"btn2 = {btn2.value()}")
    
def check_btn3(timer):
    global btn3
    print(f"btn3 = {btn3.value()}")

start = time.time()
tim1 = Timer(freq=1, mode=Timer.PERIODIC, callback=check_btn1)
tim2 = Timer(freq=0.5, mode=Timer.PERIODIC, callback=check_btn2)
tim3 = Timer(freq=2, mode=Timer.PERIODIC, callback=check_btn3)
time.sleep(20)
tim1.deinit()
tim2.deinit()
tim3.deinit()

%serialconnect 

from machine import Pin
import time

btn = Pin(20, Pin.IN)
led = Pin(25, Pin.OUT)

start = time.time()

def btn_isr(_):
    led.toggle()
    
btn.irq(btn_isr, trigger=Pin.IRQ_FALLING)

%serialconnect 

from machine import Pin, PWM
import time

btn20 = Pin(20, Pin.IN)
btn21 = Pin(21, Pin.IN)

led = Pin(25, Pin.OUT)
buzzer = PWM(Pin(18, Pin.OUT))

start = time.time()

def btn20_isr(_):
    led.toggle()
    
buzzer_on = False
buzzer.freq(500)
def btn21_isr(_):
    global buzzer_on
    if buzzer_on:
        buzzer.duty_u16(0)
        buzzer_on = False
    else:
        buzzer.duty_u16(1000)
        buzzer_on = True
    
btn20.irq(btn20_isr, trigger=Pin.IRQ_FALLING)
btn21.irq(btn21_isr, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

%serialconnect

from machine import Pin
import time

class Button(object):
    def __init__(self, gpio):
        self.btn = Pin(gpio, Pin.IN)
        # set up IRQ
        self.btn.irq(self.isr, trigger=Pin.IRQ_FALLING)
        # flag and data
        self.pressed = False
        self.time_pressed = time.ticks_ms()
        
    def isr(self, t):
        self.pressed = True
        self.time_pressed = time.ticks_ms()
        
btn = Button(20)
start = time.ticks_ms()
for k in range(10):
    if btn.pressed:
        print(btn.time_pressed - start)
        btn.pressed = False
    time.sleep(1)
