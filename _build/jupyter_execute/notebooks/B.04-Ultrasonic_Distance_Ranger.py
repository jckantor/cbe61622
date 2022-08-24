#!/usr/bin/env python
# coding: utf-8

# # Ultrasonic Distance Ranger
# 
# Create a simple rangefinder that reports distance, measured in millimeters, to a real-time display.

# ## Particle CLI

# ### Installation

# In[2]:


get_ipython().run_cell_magic('capture', '', '!bash <( curl -sL https://particle.io/install-cli )')


# ### Utility functions

# In[3]:


import re
import subprocess

# regular expression to strip ansi control characters
ansi = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

# decode byte string and strip ansi control characters
def decode_bytes(byte_string):
    if isinstance(byte_string, bytes):
        result = byte_string.decode("utf-8")
    return ansi.sub("", result)

# streamline call to the particle-cli
def particle(args, particle_cli="/root/bin/particle"):
    process = subprocess.run([particle_cli] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    process.stdout = decode_bytes(process.stdout)
    process.stderr = decode_bytes(process.stderr)
    return process


# ### Login to Particle

# In[4]:


import getpass

# prompt for username and password
username = getpass.getpass(prompt="Username: ")
password = getpass.getpass(prompt="Password: ")

# attempt login
output = particle(["login", "--username", username, "--password", password])

# report results
if output.returncode:
    print(f"Return code = {output.returncode}")
    print(output.stderr)
else:
    print(output.stdout)


# ### Select a device
# 
# The following cell downloads a list of all user devices and creates a list of device names. Here we choose the first name in the list for the rest of this notebook. If this is not the device to be used, then modify this cell accordingly.

# In[5]:


devices = [line.split()[0] for line in particle(["list"]).stdout.splitlines()]
device_name = devices[0]
print(particle(["list", device_name]).stdout)


# ## Project Hardware

# ### Grove Ultrasonic Ranger
# 
# [SeeedStudio description](https://wiki.seeedstudio.com/Grove-Ultrasonic_Ranger/)
# 
# ![](https://files.seeedstudio.com/wiki/Grove_Ultrasonic_Ranger/img/Ultrasonic.jpg)
# 
# The Grove Ultrasonic Ranger emits a sequence of eight short bursts of 40 kHz sonic signals, then measures duration until an echo is detected. The sonic signals are triggered by applying a 10 microsecond pulse to the GPIO pin connecting to the device. The duration until echo detection is returned as a pulse on the same GPIO pin. The pulse duration can be measured using the [pulseIn()](https://docs.particle.io/reference/device-os/firmware/argon/#pulsein-) function of the standard Arduino or Particle API.
# 

# ### Grove 4 Digit Display

# ## Implementation

# ### Create Project

# In[6]:


print(particle(["project", "create", "--name", "myproject", "."]).stdout)


# ### Change working directory
# 
# The Particle CLI assumes one is working in the top  project directory.

# In[7]:


get_ipython().run_line_magic('cd', '/content/myproject')


# ### Add relevant libraries

# In[8]:


print(particle(["library", "add", "Grove_4Digit_Display"]).stdout)


# ### Create source file

# In[19]:


get_ipython().run_cell_magic('writefile', 'src/myproject.ino', '\n/* Grove 4 digit display */\nconst int pinCLK = D2;         /* display clock pin */\nconst int pinDIO = D3;         /* display data pin */\nconst int digits = 4;          /* display digits */\n\n#include "Grove_4Digit_Display.h"\nTM1637 tm1637(pinCLK, pinDIO);\n\n/* Grove ultrasonic ranger */\nconst int pinULTRASONIC = D4;  /* ultrasonic ranger pin */\n\nvoid setup() {\n    /* setup display */\n    tm1637.init();\n    tm1637.set(BRIGHT_TYPICAL);\n    tm1637.point(POINT_OFF);\n}\n\nvoid loop() {\n    display(measureDistance(pinULTRASONIC));\n    delay(100);\n}\n\nvoid display(unsigned int number) {\n    for (int i = 0; i < 4; i++) {\n        int digit = digits - 1 - i;\n        tm1637.display(digit, number % 10);\n        number /= 10;\n    }\n}\n\nint measureDistance(int pin) {\n    /* send a pulse */\n    pinMode(pin, OUTPUT);\n    digitalWrite(pin, LOW);\n    delayMicroseconds(2);\n    digitalWrite(pin, HIGH);\n    delayMicroseconds(10);\n    digitalWrite(pin, LOW);\n\n    /* measure duration of response pulse in microseconds */\n    pinMode(pin, INPUT);\n    unsigned long duration = pulseIn(pin, HIGH);\n\n    /* distance in mm = 0.344 mm/micro-sec` * duration / 2 */\n    return(0.172*duration);\n}')


# ### Compiling

# In[20]:


print(particle(["compile", "argon", "--saveTo", "myproject.bin"]).stdout)


# ### Flash firmware

# In[21]:


print(particle(["flash", device_name, "myproject.bin"]).stdout)


# In[ ]:




