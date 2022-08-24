#!/usr/bin/env python
# coding: utf-8

# # Particle Command Line Interface (CLI)
# 
# This notebook demonstrates the use of the [Particle command line interface](https://docs.particle.io/reference/developer-tools/cli/) to 
# 
# * login and access a device,
# * create a project,
# * add a library,
# * prepare and save code,
# * compile the code to firmware, and
# * flash the firmware over the air.
# 
# This notebook is designed to be opened and run on Google Colab. Several modifications will be needed to run in another environment.

# ## Particle CLI

# ### Installation

# In[1]:


get_ipython().run_cell_magic('capture', '', '!bash <( curl -sL https://particle.io/install-cli )\n\n# path to the particle cli. May be environment dependent.\nparticle_cli = "/root/bin/particle"')


# In[5]:


partiicle_cli = "/Users/bin/particle"


# ### Utility functions

# In[8]:


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
    process = subprocess.run(["/Users/jeff/bin/particle"] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    process.stdout = decode_bytes(process.stdout)
    process.stderr = decode_bytes(process.stderr)
    return process

# print the default help message
print(particle(["help"]).stderr)


# ### Login to Particle

# In[9]:


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


# ## Project: Timer display
# 
# To demonstrate use of the Paricle CLI, for this project we will create a simple timer display using the [Grove 4-Digit Display](https://wiki.seeedstudio.com/Grove-4-Digit_Display/) that is shipped with the [Argon Starter Kit](https://store.particle.io/collections/prototyping-hardware/products/iot-starter-kit) available from Particle.io. The goal of the project is to display time since start device startup measure in seconds. The display will show seconds to two decimal digits for up to 100 seconds. The timer and display will roll over after 100 seconds.

# ### Particle Argon
# 
# ![](https://docs.particle.io/assets/images/argon/argon-pin-markings.png)

# ### Grove 4-Digit Display
# 
# [Grove 4-Digit Display](https://wiki.seeedstudio.com/Grove-4-Digit_Display/)  
# 
# [Documentation](https://github.com/Seeed-Studio/Grove_4Digital_Display)
# 
# ![](https://files.seeedstudio.com/wiki/Grove-4-Digit_Display/img/Grove-4_digit_display.jpg)

# ### Grove Shield FeeatherWing
# 
# Connect the Grove 4-digit display to connector D2 on the Grove Shield FeatherWing adapater.
# 
# ![](https://cdn-shop.adafruit.com/1200x900/4309-05.jpg)

# ### Create Project

# In[5]:


print(particle(["project", "create", "--name", "display4", "."]).stdout)


# ### Change working directory
# 
# The Particle CLI assumes one is working in the top  project directory.

# In[6]:


get_ipython().run_line_magic('cd', 'display4')


# ### Add relevant libraries

# In[7]:


library = "Grove_4Digit_Display"
print(particle(["library", "add", library]).stdout)


# ### Create source file

# In[8]:


get_ipython().run_cell_magic('writefile', 'src/display4.ino', '\n#define CLK D2     /* display clock pin */\n#define DIO D3     /* display data pin */\n#define DIGITS 4   /* number of display digits */\n\n#include "Grove_4Digit_Display.h"\n\nTM1637 tm1637(CLK, DIO);\nunsigned long start;\n\nvoid setup() {\n    tm1637.init();\n    tm1637.set(BRIGHT_TYPICAL);\n    tm1637.point(POINT_ON);\n    start = millis();\n}\n\nvoid loop() {\n    unsigned long time = (millis() - start) % 100000;\n    display(time / 10); /* displaying 100th\'s of seconds */\n}\n\nvoid display(unsigned int number) {\n    for (int i = 0; i < 4; i++) {\n        int digit = DIGITS - 1 - i;\n        if (number != 0) {\n            tm1637.display(digit, number % 10);\n        } else {\n            tm1637.display(digit, 0x7f); /* display blank */\n        }\n        number /= 10;\n    }\n}')


# ### Compiling

# In[9]:


print(particle(["compile", "argon", "--saveTo", "display4.bin"]).stdout)


# ### Flash firmware

# In[10]:


print(particle(["flash", device_name, "display4.bin"]).stdout)


# 
