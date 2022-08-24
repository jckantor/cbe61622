#!/usr/bin/env python
# coding: utf-8

# # Particle Command Line Interface
# 
# The Particle Argon is a microcontroller board similar to an Arduino in concept but with extended wifi and cloud support.
# 
# ![Particle Argon](https://images.ctfassets.net/ity165ek7v1z/5x0EeKXhRxrgA2Ebgnqnik/654abeb410afd7f10fd3f99b5d871599/prototype.jpeg?w=510&h=340&q=80&fm=webp)
# 
# The [Particle command line interface](https://docs.particle.io/tutorials/developer-tools/cli/) provides is a javascript based library exposing much of the Particle device functionality. This notebook shows how the command line interface can be use within Google Colab notebook.

# ## Installation of the Particle command line interface

# In[ ]:


get_ipython().run_cell_magic('capture', '', '!bash <( curl -sL https://particle.io/install-cli )')


# ## Login to Particle

# In[ ]:


import getpass
import subprocess

particle_cli = "/root/bin/particle"
username = getpass.getpass(prompt="Username: ")
password = getpass.getpass(prompt="Password: ")

process = subprocess.run([particle_cli, "login",
                          "--username", username,
                          "--password", password],
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)

if process.stderr.decode("utf-8"):
    print(process.stderr.decode("utf-8"))
else:
    print(f"Successfully logged in to Particle Device Cloud as {username}")
    process = subprocess.run([particle_cli, "list"], stdout=subprocess.PIPE)
    print(process.stdout.decode("utf-8"))


# ## Demonstrations

# ### Flashing Tinker firmware
# 
# [Tinker](https://docs.particle.io/tutorials/developer-tools/tinker/photon/) is the default firmware that ships with Particle devices. The following cell restores the device to the factory default by flashing tinker.

# In[ ]:


device_name = "jck_argon_01"


# In[ ]:


process = subprocess.run([particle_cli, "flash", device_name, "tinker"], stdout=subprocess.PIPE)
print(process.stdout.decode("utf-8"))


# ### Toggle on-board led

# In[ ]:


import time
import os
import subprocess

led = "D7"

# digital write
def digitalwrite(device_name, pin, value):
    process = subprocess.run([particle_cli, "call", device_name, "digitalwrite",
                              f"{pin},{value}"], 
                             stdout=subprocess.PIPE, 
                             stderr=subprocess.PIPE)
    return process.stdout.decode("utf-8")

# loop and toggle
for k in range(0, 5):
    digitalwrite(device_name, led, "HIGH")
    time.sleep(0.5)
    digitalwrite(device_name, led, "LOW")


# ### Reading Grove Light Sensor V1.2
# 
# The Grove Light Sensor V1.2 to pin 
# 
# ![](https://static-cdn.seeedstudio.site/media/catalog/product/cache/9d0ce51a71ce6a79dfa2a98d65a0f0bd/h/t/httpsstatics3.seeedstudio.comseeedimg2016-10po8b7qd0xnlnchgogziq9g3d.jpg)

# In[ ]:


import time
import os
import subprocess
import re

device_name = "jck_argon_01"
light_sensor = "A2"

def read_ansi(byte_str):
    """Decode a byte string and remove any ANSI control codes."""
    return re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', byte_str.decode("utf-8"))

# analog read
def analogread(device_name, pin):
    process = subprocess.run([particle_cli, "call", device_name, "analogread",  f"{pin}"], 
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return int(read_ansi(process.stdout))

analogread(device_name, light_sensor)


# 
