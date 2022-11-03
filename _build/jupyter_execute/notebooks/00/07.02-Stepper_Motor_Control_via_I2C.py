#!/usr/bin/env python
# coding: utf-8

# # Stepper Motor Control via I2C
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

# In[ ]:


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

# In[ ]:


devices = [line.split()[0] for line in particle(["list"]).stdout.splitlines()]
device_name = devices[0]
print(particle(["list", device_name]).stdout)


# ## Project: Motor Control
# 
# 

# ### Grove I2C Motor Driver V1.3
# 
# [SeeedStudio Documentation](https://wiki.seeedstudio.com/Grove-I2C_Motor_Driver_V1.3/)
# 
# [Github repository](https://github.com/Seeed-Studio/Grove_I2C_Motor_Driver_v1_3)
# 
# ![](https://files.seeedstudio.com/wiki/Grove-I2C_Motor_Driver_V1.3/img/I2CMotorDriver-1.jpg)
# 
# Note the default address ``0x0f``.
# 
# ** It turns out this motor driver requires a 5 volt logic. The Particle Argon is capable of 3.3v only, thus not electrically compatible. This is confirmed by the absence of a code library supporting this motor driver on Particle Argon.**
# 
# **New motor drivers are on order.**

# ## Prototype

# ### Create Project

# In[ ]:


print(particle(["project", "create", "--name", "myproject", "."]).stdout)


# ### Change working directory
# 
# The Particle CLI assumes one is working in the top  project directory.

# In[ ]:


get_ipython().run_line_magic('cd', 'myproject')


# ### Add relevant libraries
# 
# 

# In[ ]:


print(particle(["library", "search", "motor"]).stdout)


# In[ ]:


print(particle(["library", "add", "Grove_I2C_Motor_Driver_v1_3"]).stdout)


# ### Create source file

# In[ ]:


get_ipython().run_cell_magic('writefile', 'src/myproject.ino', '')


# ### Compiling

# In[ ]:


print(particle(["compile", "argon", "--saveTo", "myproject.bin"]).stdout)


# ### Flash firmware

# In[ ]:


print(particle(["flash", device_name, "myproject.bin"]).stdout)

