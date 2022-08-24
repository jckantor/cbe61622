%serialconnect

from machine import Pin
import time
from rp2 import PIO, StateMachine, asm_pio

# decorator to translate to PIO machine code
@asm_pio(
    out_init = (rp2.PIO.OUT_LOW,) * 8,     # initialize 8 consecutive pins
    out_shiftdir = rp2.PIO.SHIFT_RIGHT)    # output lsb bits first

def parallel_prog():
    pull(block)                             # pull data from Tx FIFO. Wait for data
    out(pins, 8)                            # send 8 bits from OSR to pins

# create an instance of the state machine
sm = StateMachine(0, parallel_prog, freq=1000000, out_base=Pin(0))

# start the state machine
sm.active(1)

for n in range(256):
    sm.put(n)
    time.sleep(0.01)


%serialconnect

from machine import Pin
import time
from rp2 import PIO, StateMachine, asm_pio

# decorator to translate to PIO machine code
@asm_pio(
    out_init = (rp2.PIO.OUT_LOW,) * 4,     # initialize 8 consecutive pins
    out_shiftdir = rp2.PIO.SHIFT_RIGHT)    # output lsb bits first

def stepper_step():
    pull(block)                             # pull data from Tx FIFO. Wait for data
    out(pins, 4)                            # send 8 bits from OSR to pins

# create an instance of the state machine
sm = StateMachine(0, stepper_step, freq=1000000, out_base=Pin(0))

# start the state machine
sm.active(1)

step_sequence = [8, 12, 4, 6, 2, 3, 1, 9]
 
for n in range(500):
    sm.put(step_sequence[n % len(step_sequence)])
    time.sleep(0.01)

%serialconnect

from machine import Pin
import time
from rp2 import PIO, StateMachine, asm_pio

# decorator to translate to PIO machine code
@asm_pio(
    set_init = rp2.PIO.OUT_LOW)

def count_blink():
    pull()
    mov(x, osr)
    label("count")
    set(pins, 1)
    set(y, 100)
    label("on")
    nop()        [1]
    jmp(y_dec, "on")
    set(pins, 0)
    nop()        [19]
    nop()        [19]
    nop()        [19]
    nop()        [19]
    jmp(x_dec, "count")

# create an instance of the state machine
sm = StateMachine(0, count_blink, freq=2000, set_base=Pin(25))

# start the state machine
sm.active(1)
sm.put(20)


%serialconnect

from machine import Pin
import time
from rp2 import PIO, StateMachine, asm_pio

# decorator to translate to PIO machine code
@asm_pio(
    out_init = (rp2.PIO.OUT_LOW,) * 4,     # initialize 8 consecutive pins
    out_shiftdir = rp2.PIO.SHIFT_RIGHT)    # output lsb bits first

def stepper_step():
    pull(block)                             # pull data from Tx FIFO. Wait for data
    out(pins, 4)                            # send 8 bits from OSR to pins

# create an instance of the state machine
sm = StateMachine(0, stepper_step, freq=1000000, out_base=Pin(0))

# start the state machine
sm.active(1)

step_sequence = [8, 12, 4, 6, 2, 3, 1, 9]

def step():
    pos = 0
    while True:
        coils = step_sequence[pos % len(step_sequence)]
        yield coils
        pos += 1
        
stepper = step()
for k in range(10):
    c = next(stepper)
    print(c)
    


#for n in range(100):
#    for step in step_sequence:
#        sm.put(step)
#        time.sleep(0.01)

%serialconnect

from machine import Pin
import time
import rp2
from rp2 import PIO, StateMachine, asm_pio

@asm_pio(out_init = rp2.PIO.OUT_LOW)
def count_blink():
    pull(block)            # wait for data on Tx FIFO
    set(pins, 1)
    set(x, osr)
    
# create an instance of the state machine
sm0 = StateMachine(0, count_blink, freq=2000, out_base=Pin(25))

# start the state machine
sm0.active(1)
sm0.put(1)
time.sleep(2)
sm0.active(0)

%serialconnect

from machine import Pin
import time
from rp2 import PIO, StateMachine, asm_pio

# decorator to translate to PIO machine code
@asm_pio(
    out_init = (rp2.PIO.OUT_LOW,) * 4,     # initialize 8 consecutive pins
    out_shiftdir = rp2.PIO.SHIFT_RIGHT)    # output lsb bits first

def stepper_step():
    pull(block)                             # pull data from Tx FIFO. Wait for data
    out(pins, 4)                            # send 8 bits from OSR to pins

# create an instance of the state machine
sm = StateMachine(0, stepper_step, freq=1000000, out_base=Pin(0))

# start the state machine
sm.active(1)

step_sequence = [8, 12, 4, 6, 2, 3, 1, 9]
 
for n in range(1000):
    sm.put(step_sequence[n % len(step_sequence)])
    time.sleep(0.01)
        


