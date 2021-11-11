##
from machine import Pin
import time
import rp2
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(out_init = rp2.PIO.OUT_LOW)
def count_blink():
    pull(block)
    set(pins, 1) [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    set(pins, 0) [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    
# create an instance of the state machine
sm0 = StateMachine(0, count_blink, freq=2000, out_base=Pin(0))

# start the state machine
sm0.active(1)    
sm0.put(1)
time.sleep(2)
sm0.active(0)
    
    