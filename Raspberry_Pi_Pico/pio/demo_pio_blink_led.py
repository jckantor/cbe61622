# Demonstrate PIO using the on-board LED

# Method 1.  Polling with utime.sleep() to schedule on/off transitions

import machine
import utime

led = machine.Pin(25, mode=machine.Pin.OUT)
period = 100

print("Polling loop.")
start = utime.ticks_ms()
while utime.ticks_ms() < start + 5000:
    led.value(0)
    utime.sleep_ms(int(period/2))
    led.value(1)
    utime.sleep_ms(int(period/2))
led.value(0)

# Method 2. Use Timer

def toggle_led(timer):
    global led
    led.toggle()

print("Timer interrupts.")
# run the blinker for period milliseconds
timer = machine.Timer(period=int(period/2), mode=machine.Timer.PERIODIC, callback=toggle_led)
utime.sleep_ms(5000)
timer.deinit()

# Method 3. Use PIO
print("PIO")

import machine
import utime
import rp2

@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
def blink():
    wrap_target()         # start of a loop
    set(pins, 1) [31]     # set base pio to 1, then wait 31 cycles
    nop() [31]            # wait 32 more cycles
    nop() [31]
    nop() [3]
    set(pins, 0) [31]     # set base pin to 0, then wait 31 cycles
    nop() [31]            # wait 32 more cycles
    nop() [31]            # wait 32 more cycles
    nop() [31]
    nop() [3]
    wrap()
    
sm = rp2.StateMachine(0, blink, freq=2000, set_base=led)

sm.active(1)
utime.sleep_ms(5000)
sm.active(0)

