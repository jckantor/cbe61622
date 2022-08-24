#!/usr/bin/env python
# coding: utf-8

# # Getting Started with Pymata4
# 
# [Pymata4](https://github.com/MrYsLab/pymata4) is a Python library that allows you to monitor and control Arduino hardware from a host computer. The library uses the Firmata protocol for communicating with the Arduino hardware. Pymata4 supports the StandardFirmata server included with the Arduino IDE, and also StandardFirmataWiFi, and an enhanced server FirmataExpress distributed with Pymata4.
# 
# Pymata4 uses [concurrent Python threads](https://mryslab.github.io/pymata4/concurrency/) to manage interaction with the Arduino. The concurrency model enables development of performant and interactive Arduino applications using Python on a host computer. Changes in the status of an Arduino pin can be processed with callbacks. It's sibling, [pymata-express](https://github.com/MrYsLab/pymata-express), is available using the [Python asyncio package](https://docs.python.org/3/library/asyncio.html).
# 
# Support for common $I^2C$ devices, including stepper motors, is included in FirmataExpress. Applications using unsupported $I^2C$ devices may require [modifications to the Firmata server sketch](https://www.instructables.com/Going-Beyond-StandardFirmata-Adding-New-Device-Sup/). 
# 
# Useful links:
# * [Pymata4 API documentation](http://htmlpreview.github.io/?https://raw.githubusercontent.com/MrYsLab/pymata4/master/html/pymata4/index.html)

# ## Hardware Setup and Software Installations
# 
# The Arduino must be attached to the host by USB with either the StandardFirmata or Firmata-express sketch installed using the Arduino IDE. For use with WiFi, install StandardFirmataWiFi.
# 
# The Python pymata4 package can be installed with pip.

# In[24]:


get_ipython().system('pip install pymata4')


# ## Basic Usage
# 
#     pymata4.Pymata()
#     board.shutdown()

# In[4]:


from pymata4 import pymata4

# create a board instance
board = pymata4.Pymata4()

# remember to shutdown
board.shutdown()


# ## Blinker
# 
#     board.digital_write(pin, value)
# 
# Pymata4 has two methods for writing a 1 or a 0 to a digital output.  `digital_write(pin, value)` hides details of the Firmata protocol from the user. The user can refer to digital pins just as they would in standard Arduino coding. A second method, `digital_pin_write(pin, value)` allows writing to multiples at the same time, but requires the user to understand further details of the Firmata protocol.

# In[5]:


from pymata4 import pymata4
import time

LED_PIN = 13

board = pymata4.Pymata4()

# set the pin mode
board.set_pin_mode_digital_output(LED_PIN)

for n in range(5):
    print("LED ON")
    board.digital_write(LED_PIN, 1)
    time.sleep(1)
    
    print("LED OFF")
    board.digital_write(LED_PIN, 0)
    time.sleep(1)

board.shutdown()


# ## Handling a Keyboard Interrupt
# 
# Pymata4 sets up multiple concurrent processes upon opening connection to the Arduino hardware. If Python execution is interrupted, it isimportant to catch the interrupt and shutdown the board before exiting the code. Otherwise the Arduino may continue to stream data requiring the Arduino to be reset.

# In[23]:


from pymata4 import pymata4
import time

def blink(board, pin, N=20):
    board.set_pin_mode_digital_output(LED_PIN)
    for n in range(N):
        board.digital_write(LED_PIN, 1)
        time.sleep(0.5)
        board.digital_write(LED_PIN, 0)
        time.sleep(0.5)
    board.shutdown()
    
LED_PIN = 13
board = pymata4.Pymata4() 

try:
    blink(board, LED_PIN)
except KeyboardInterrupt:
    print("Operation interrupted. Shutting down board.")
    board.shutdown()


# ## Getting Information about the Arduino
# 
# [Firmata protocol](https://github.com/firmata/protocol/blob/master/protocol.md)

# In[38]:


from pymata4 import pymata4
import time

board = pymata4.Pymata4()

print("Board Report")
print(f"Firmware version: {board.get_firmware_version()}")
print(f"Protocol version: {board.get_protocol_version()}")
print(f"Pymata version: {board.get_pymata_version()}")

def print_analog_map(board):
    analog_map = board.get_analog_map()
    for pin, apin in enumerate(analog_map):
        if apin < 127:
            print(f"Pin {pin:2d}: analog channel = {apin}")

def print_pin_state_report(board):
    pin_modes = {
        0x00: "INPUT",
        0x01: "OUTPUT",
        0x02: "ANALOG INPUT",
        0x03: "PWM OUTPUT",
        0x04: "SERVO OUTPUT",
        0x06: "I2C",
        0x08: "STEPPER",
        0x0b: "PULLUP",
        0x0c: "SONAR",
        0x0d: "TONE",
    }
    analog_map = board.get_analog_map()
    for pin in range(len(analog_map)):
        state = board.get_pin_state(pin)
        print(f"Pin {pin:2d}: {pin_modes[state[1]]:>15s} = {state[2]}")
    
print_pin_state_report(board)
board.digital_write(13, 1)
print_pin_state_report(board)
print_analog_map(board)

capability_report = board.get_capability_report()

board.shutdown()

# get capability report
print("\nCapability Report")
modes = {
    0x00: "DIN",  # digital input
    0x01: "DO",   # digital output
    0x02: "AIN",  # analog input
    0x03: "PWM",  # pwm output
    0x04: "SRV",  # servo output
    0x05: "SFT",  # shift
    0x06: "I2C",  # I2C
    0x07: "WIR",  # ONEWIRE
    0x08: "STP",  # STEPPER
    0x09: "ENC",  # ENCODER
    0x0A: "SRL",  # SERIAL
    0x0B: "INP",  # INPUT_PULLUP
}

pin_report = {}
pin = 0
k = 0
while k < len(capability_report):
    pin_report[pin] = {}
    while capability_report[k] < 127:
        pin_report[pin][modes[capability_report[k]]] = capability_report[k+1]
        k += 2
    k += 1
    pin += 1

mode_set = set([mode for pin in pin_report.keys() for mode in pin_report[pin].keys()])
print("        " + "".join([f" {mode:>3s} " for mode in sorted(mode_set)]))
for pin in pin_report.keys():
    s = f"Pin {pin:2d}:"
    for mode in sorted(mode_set):
        s += f" {pin_report[pin][mode]:>3d} " if mode in pin_report[pin].keys() else " "*5
    print(s)


# ## Temperature Control Lab Shield

# In[44]:


from pymata4 import pymata4
import time

class tclab():
    def __init__(self):
        self.board = pymata4.Pymata4()
        self.LED_PIN = 9
        self.Q1_PIN = 3
        self.Q2_PIN = 5
        self.T1_PIN = 0
        self.T2_PIN = 2
        self.board.set_pin_mode_pwm_output(self.LED_PIN)
        self.board.set_pin_mode_pwm_output(self.Q1_PIN)
        self.board.set_pin_mode_pwm_output(self.Q2_PIN)
        self.board.set_pin_mode_analog_input(self.T1_PIN)
        self.board.set_pin_mode_analog_input(self.T2_PIN)
        self._Q1 = 0
        self._Q2 = 0
        time.sleep(0.1)
        
    def __enter__(self): 
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return
    
    def close(self):
        self.Q1(0)
        self.Q2(0)
        self.board.shutdown()
    
    def read_temperature(self, pin):
        # firmata doesn't provide a means to use the 3.3 volt reference
        adc, ts = self.board.analog_read(pin)
        return round(adc*513/1024 - 50.0, 1)
    
    def Q1(self, val):
        val = int(255*max(0, min(100, val))/100)
        self.board.pwm_write(self.Q1_PIN, val)
        
    def Q2(self, val):
        val = int(255*max(0, min(100, val))/100)
        self.board.pwm_write(self.Q2_PIN, val)
    
    def T1(self):
        return self.read_temperature(self.T1_PIN)
    
    def T2(self):
        return self.read_temperature(self.T2_PIN)
        
    def LED(self, val):
        val = max(0, min(255, int(255*val/100)))
        self.board.pwm_write(self.LED_PIN, val)
        
with tclab() as lab:
    lab.Q1(100)
    lab.Q2(100)
    for n in range(30):
        print(lab.T1(), lab.T2())
        lab.LED(100)
        time.sleep(0.5)
        lab.LED(0)
        time.sleep(0.5)
    lab.Q1(0)
    lab.Q2(0)


# In[ ]:




