# parallel byte from data

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from utime import sleep


@asm_pio(out_init = (rp2.PIO.OUT_HIGH,)*8,
         out_shiftdir = PIO.SHIFT_RIGHT,
         autopull = True,
         pull_thresh = 16)
def paral_prog():
    pull
    out(pins, 8)
    
sm = StateMachine(0, paral_prog, freq=10000000, out_base=Pin(0))
sm.active(1)

while True:
    for i in range(500):
        sm.put(i)
#        print(i)
#        sleep(0.01)