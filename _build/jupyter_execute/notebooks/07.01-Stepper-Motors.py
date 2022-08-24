%serialconnect

from machine import Pin
import time

class Stepper(object):
    
    step_seq = [[1, 0, 0, 0], 
                [1, 1, 0, 0], 
                [0, 1, 0, 0],
                [0, 1, 1, 0],
                [0, 0, 1, 0],
                [0, 0, 1, 1], 
                [0, 0, 0, 1], 
                [1, 0, 0, 1]]
    
    def __init__(self, gpio_pins):
        self.pins = [Pin(pin, Pin.OUT) for pin in gpio_pins]
        self.motor_position = 0
        
    def rotate(self, degrees=360):
        n_steps = abs(int(4075.7728*degrees/360))
        d = 1 if degrees > 0 else -1
        for _ in range(n_steps):
            self.motor_position += d
            phase = self.motor_position % len(self.step_seq)
            for i, value in enumerate(self.step_seq[phase]):
                self.pins[i].value(value)
            time.sleep(0.001)                
        
stepper = Stepper([2, 3, 4, 5])
stepper.rotate(360)
stepper.rotate(-360)
print(stepper.motor_position)

%serialconnect

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4)
def prog():
    wrap_target()
    set(pins, 8) [31] # 8
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 4) [31] # 4
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 2) [31] # 2
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    set(pins, 1) [31] # 1
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    nop() [31]
    wrap()
    

sm = StateMachine(0, prog, freq=100000, set_base=Pin(14))


sm.active(1)
sleep(10)
sm.active(0)
sm.exec("set(pins,0)")

%serialconnect

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_HIGH,) * 4,
         out_shiftdir=PIO.SHIFT_LEFT)
def prog():
    pull()
    mov(y, osr) # step pattern
    
    pull()
    mov(x, osr) # num steps
    
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    nop() [31]
    nop() [31]
    nop() [31]

    jmp(x_dec,"loop")
    label("end")
    set(pins, 8) [31] # 8

sm = StateMachine(0, prog, freq=10000, set_base=Pin(14), out_base=Pin(14))

sm.active(1)
sm.put(2216789025) #1000 0100 0010 0001 1000010000100001
sm.put(1000)
sleep(10)
sm.active(0)
sm.exec("set(pins,0)")


%serialconnect

from machine import Pin
from rp2 import PIO, StateMachine, asm_pio
from time import sleep
import sys

@asm_pio(set_init=(PIO.OUT_LOW,) * 4,
         out_init=(PIO.OUT_LOW,) * 4,
         out_shiftdir=PIO.SHIFT_RIGHT,
         in_shiftdir=PIO.SHIFT_LEFT)
def prog():
    pull()
    mov(x, osr) # num steps
    
    pull()
    mov(y, osr) # step pattern
    
    jmp(not_x, "end")
    
    label("loop")
    jmp(not_osre, "step") # loop pattern if exhausted
    mov(osr, y)
    
    label("step")
    out(pins, 4) [31]
    
    jmp(x_dec,"loop")
    label("end")
    
    irq(rel(0))


sm = StateMachine(0, prog, freq=10000, set_base=Pin(14), out_base=Pin(14))
data = [(1,2,4,8),(2,4,8,1),(4,8,1,2),(8,1,2,4)]
steps = 0

def turn(sm):
    global steps
    global data
    
    idx = steps % 4
    a = data[idx][0] | (data[idx][1] << 4) | (data[idx][2] << 8) | (data[idx][3] << 12)
    a = a << 16 | a
    
    #print("{0:b}".format(a))
    sleep(1)
    
    sm.put(500)
    sm.put(a)
    
    steps += 500

sm.irq(turn)
sm.active(1)
turn(sm)

sleep(50)
print("done")
sm.active(0)
sm.exec("set(pins,0)")


%serialconnect
   
import time
import rp2

@rp2.asm_pio()
def irq_test():
    wrap_target()
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    irq(0)
    nop()          [31]
    nop()          [31]
    nop()          [31]
    nop()          [31]
    irq(1)
    wrap()


rp2.PIO(0).irq(lambda pio: print(pio.irq().flags()))
#rp2.PIO(1).irq(lambda pio: print("1"))

sm = rp2.StateMachine(0, irq_test, freq=2000)
sm1 = rp2.StateMachine(1, irq_test, freq=2000)
sm.active(1)
#sm1.active(1)
time.sleep(1)
sm.active(0)
sm1.active(0)


