#!/usr/bin/env python
# coding: utf-8

# # Simple Stop Watch using Interrupts
# 

# ## Particle CLI

# ### Installation

# In[1]:


get_ipython().run_cell_magic('capture', '', '!bash <( curl -sL https://particle.io/install-cli )\n\n# path to the particle cli. May be environment dependent.\nparticle_cli = "/root/bin/particle"')


# ### Utility functions

# In[2]:


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
def particle(args):
    process = subprocess.run(["/root/bin/particle"] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    process.stdout = decode_bytes(process.stdout)
    process.stderr = decode_bytes(process.stderr)
    return process


# ### Login to Particle

# In[3]:


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

# In[4]:


devices = [line.split()[0] for line in particle(["list"]).stdout.splitlines()]
device_name = devices[0]
print(particle(["list", device_name]).stdout)


# ## Project: Simple Stop Watch
# 
# The goal of this project is to build a simple stop watch. The project will use code previously developed for the Grove 4 digit display, and add a Grove button to control operation of the stop watch. The stop watch will start and stop with a short click of the button, and reset to zero with a long button press.
# 

# ### Grove Button
# 
# The Grove Button is a momentary contact with a [pull-down resistor](https://www.seeedstudio.com/blog/2020/02/21/pull-up-resistor-vs-pull-down-differences-arduino-guide/). With a pull-down resistor, the pin value is LOW when the button is not pressed, and become HIGH when the button is depressed. 

# ## Solution 1: Using clickButton library

# ### Create Project

# In[5]:


print(particle(["project", "create", "--name", "myproject", "."]).stdout)


# ### Change working directory
# 
# The Particle CLI assumes one is working in the top  project directory.

# In[6]:


get_ipython().run_line_magic('cd', 'myproject')


# ### Add relevant libraries

# In[7]:


print(particle(["library", "add", "Grove_4Digit_Display"]).stdout)
print(particle(["library", "add", "clickButton"]).stdout)


# ### Create source file

# In[9]:


get_ipython().run_cell_magic('writefile', 'src/myproject.ino', '\n/* pin assignments */\n#define PIN_CLK D2     /* display clock */\n#define PIN_DIO D3     /* display data */\n#define PIN_BTN D4     /* button */\n\n/* display parameters */\n#define DIGITS 4   /* display digits */\n\n#include "Grove_4Digit_Display.h"\n#include "clickButton.h"\n\n/* display object */\nTM1637 tm1637(PIN_CLK, PIN_DIO);\n\n/* button object */\nClickButton button(PIN_BTN, HIGH);\n\n/* stopwatch state */\nunsigned long curr_time;\nunsigned long prev_time;\nunsigned long display_time;\nbool running;\n\nvoid setup() {\n    /* setup display */\n    tm1637.init();\n    tm1637.set(BRIGHT_TYPICAL);\n    tm1637.point(POINT_ON);\n\n    /* setup button */\n    pinMode(PIN_BTN, INPUT);\n    button.debounceTime = 0;\n    button.multiclickTime = 250;\n    button.longClickTime = 1000;\n\n    /* setup stopwatch */\n    prev_time = millis();\n    display_time = 0;\n    running = FALSE;\n}\n\nvoid loop() {\n    button.Update();\n    if (button.clicks > 0) {\n        running = !running;\n    } else if (button.clicks < 0) {\n        display_time = 0;\n    }\n    if (running) {\n        curr_time = millis();\n        display_time += curr_time - prev_time;\n    } else {\n        curr_time = millis();\n    }\n    prev_time = curr_time;\n    display(display_time / 10); /* displaying 100th\'s of seconds */\n}\n\nvoid display(unsigned int number) {\n    for (int i = 0; i < 4; i++) {\n        int digit = DIGITS - 1 - i;\n        tm1637.display(digit, number % 10);\n        number /= 10;\n    }\n}')


# ### Compiling

# In[10]:


print(particle(["compile", "argon", "--saveTo", "myproject.bin"]).stdout)


# ### Flash firmware

# In[11]:


print(particle(["flash", device_name, "myproject.bin"]).stdout)


# ## Solution 2: Interrupt Service Routine (ISR)
# 
# The ``clickButton`` library provides an easy-to-use method of managing the button actions, with provisions for debouncing, multiple clicks, and long clicks, but testing shows the button updates when the button is released, not when it is pressed. This is not consistent with a user's expectation that the clock should stop and start on the press of the button, not on the release.
# 
# The following cell demonstrates the use of an Interrupt Service Routine to manage the button interface. The key insight here is to respond to both the press and release of the button by specifying ``CHANGE`` in the ``attachInterrupt`` function. This makes is possible to detect a long button press to reset the stop watch display to zero.

# In[ ]:


get_ipython().run_cell_magic('writefile', 'src/myproject.ino', '\n/* pin assignments */\n#define PIN_CLK D2     /* display clock */\n#define PIN_DIO D3     /* display data */\n#define PIN_BTN D4     /* button */\n\n/* display parameters */\n#define DIGITS 4   /* display digits */\n\n#include "Grove_4Digit_Display.h"\n#include "clickButton.h"\n\n/* display object */\nTM1637 tm1637(PIN_CLK, PIN_DIO);\n\n/* stopwatch state */\nunsigned long curr_time;\nunsigned long prev_time;\nunsigned long display_time;\nvolatile unsigned long btn_press_time;\nvolatile bool btn_is_pressed;\nvolatile bool running;\n\nvoid setup() {\n    /* setup display */\n    tm1637.init();\n    tm1637.set(BRIGHT_TYPICAL);\n    tm1637.point(POINT_ON);\n\n    /* setup button */\n    pinMode(PIN_BTN, INPUT);\n    btn_press_time = millis();\n    attachInterrupt(PIN_BTN, on_btn_change, CHANGE);\n\n    /* setup stopwatch */\n    prev_time = millis();\n    display_time = 0;\n    running = FALSE;\n}\n\nvoid loop() {\n    curr_time = millis();\n    if (running) {\n        display_time += curr_time - prev_time;\n        if (btn_is_pressed && ((curr_time - btn_press_time) > 1000)) {\n            running = FALSE;\n            display_time = 0;\n        }\n    }\n    prev_time = curr_time;\n    display(display_time / 10); /* displaying 100th\'s of seconds */\n}\n\nvoid on_btn_change() {\n    if (digitalRead(PIN_BTN)==HIGH) {\n        if ((millis() - btn_press_time) > 50) {\n            running = !running;\n            btn_press_time = millis();\n            btn_is_pressed = TRUE;\n        }\n    } else {\n        btn_is_pressed = FALSE;   \n    }\n}\n\nvoid display(unsigned int number) {\n    for (int i = 0; i < 4; i++) {\n        int digit = DIGITS - 1 - i;\n        tm1637.display(digit, number % 10);\n        number /= 10;\n    }\n}')


# In[ ]:


print(particle(["compile", "argon", "--saveTo", "myproject.bin"]).stdout)


# In[ ]:


print(particle(["flash", device_name, "myproject.bin"]).stdout)


# In[ ]:




