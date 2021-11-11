from machine import Pin
import time



pins = [
    Pin(14, Pin.OUT), # IN1
    Pin(15, Pin.OUT), # IN2
    Pin(16, Pin.OUT), # IN3
    Pin(17, Pin.OUT), # IN4
]


full_step_sequence = [[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]]

while True:
    for step in full_step_sequence:
        for i, value in enumerate(step):
            pins[i].value(value)
        time.sleep(0.002)