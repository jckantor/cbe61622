# Introductory demonstration of PIO
#
# Description: Use the set instruction to flash the on-board led

import machine

# the pico specific libraries needed for PIO

from rp2 import PIO, StateMachine, asm_pio

# @asm_pio decorator compiles a function to PIO assembly language.
# The set_init configures and initializes pins for set instruction.
# Options are:
#     PIO.IN_HIGH
#     PIO.IN_LOW
#     PIO.OUT_HIGH
#     PIO.OUT_LOW
# Here we configure one pin for use as an output pin.

# Each PIO block can store up 32 instructions shared by four state machines.

# Set instruction: set(destination, data)
#     destination can be
#          pins
#          pindirs: 0 ==> input, 1 ==> output
#          x: scratch register
#          y: scratch register
#     data is an integer between 0 and 31

@asm_pio(set_init = (PIO.OUT_LOW,) * 5,
         sideset_init=PIO.OUT_LOW)
def square_wave():
    set(pins, 26) .side(0)
    set(pins, 0) .side(1)  [4]

# Initialize a state machine.

sm = StateMachine(0,                           # state machine 0 - 7
                  square_wave,                 # PIO function
                  freq=2000,               # PIO frequency
                  set_base=machine.Pin(0),     # set base for set instruction
                  sideset_base=machine.Pin(6)) # set base for sideset 

# activate
sm.active(1)

