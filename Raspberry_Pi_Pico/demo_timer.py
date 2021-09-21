import machine
import utime

# turn on LED
led = machine.Pin(25, machine.Pin.OUT)
led.value(1)

# working with time

tic = utime.ticks_ms()

utime.sleep(1)
utime.sleep_ms(500)
utime.sleep_us(1000)

toc = utime.ticks_ms()
delta = utime.ticks_diff(toc, tic)
print(f"elapsed time = {delta} milliseconds")

# put oscilloscope/logic analyzer on pins 00 and 01 to observe responses

print("Toggle GPIO 00 every millisecond for 10 seconds")

gp00 = machine.Pin(0, machine.Pin.OUT)
gp01 = machine.Pin(1, machine.Pin.OUT)

for n in range(10000):
    gp00.toggle()
    utime.sleep_ms(1)
gp00.value(0)

# working with Timers

print("Toggle GP00 using Timers")

def tick0(timer):
    global gp00
    gp00.toggle()
    
def tick1(timer):
    global gp01
    gp01.toggle()
    
timer0 = machine.Timer(freq=2000, mode=machine.Timer.PERIODIC, callback=tick0)
timer1 = machine.Timer(freq=2000, mode=machine.Timer.PERIODIC, callback=tick1)

# EXERCISE What is the highest frequency that can be reliably achieved?

# EXERCISE Use an oscilloscope or logic analyzer to determine the accuracy of the
# timing loop. Which gives a more reliable result ... polling or using timer interrupts?
# Quantify your answer and demonstrate with instrument traces.

# EXERCISE Add a timer to blink the on-board led once per second. The ISR should
# be called "blink_led"

def blink_led(timer):
    global led
    led.toggle()
    
timer_led = machine.Timer(freq=1, mode=machine.Timer.PERIODIC, callback=blink_led)

