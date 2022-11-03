#!/usr/bin/env python
# coding: utf-8

# # Communicating via TCP
# 
# This notebook shows how to implement a TCP Server on Particle Argon and communicate with the server from a laptop using a ``netcat`` utility.

# ## Particle CLI

# ### Installation

# In[1]:


get_ipython().run_cell_magic('capture', '', '!bash <( curl -sL https://particle.io/install-cli )')


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
def particle(args, particle_cli="/root/bin/particle"):
    process = subprocess.run([particle_cli] + args,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    process.stdout = decode_bytes(process.stdout)
    process.stderr = decode_bytes(process.stderr)
    return process


# ### Login to Particle

# ### Select a device
# 
# The following cell downloads a list of all user devices and creates a list of device names. Here we choose the first name in the list for the rest of this notebook. If this is not the device to be used, then modify this cell accordingly.

# In[6]:


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


# In[7]:


devices = [line.split()[0] for line in particle(["list"]).stdout.splitlines()]
device_name = devices[0]
print(particle(["list", device_name]).stdout)


# ## Project Considerations
# 

# ## Implementation
# 
# MacOS
# 
#     nc -4 -n 192.168.xxx.xxx pppp

# ### Create Project

# In[8]:


print(particle(["project", "create", "--name", "myproject", "."]).stdout)


# ### Change working directory
# 
# The Particle CLI assumes one is working in the top  project directory.

# In[9]:


get_ipython().run_line_magic('cd', '/content/myproject')


# ### Create source file

# In[11]:


get_ipython().run_cell_magic('writefile', 'src/myproject.ino', '\n/* \nDemonstrate bidirectional communication with Particle using TCPServer and\nclient. After flashing this firmware, check the Particle console for the local\nIP address. Connect to the local IP address using netcat\n\n    nc -4 -n 192.168.xxx.xxx 23\n\nType H and L will turn the on-board LED on and off.\n*/\n\nTCPServer server = TCPServer(23);\nTCPClient client;\n\nconst int led = D7;\nlong int timeout;\nchar c;\n\nvoid setup() {\n    server.begin();\n    Particle.publish("Server IP", WiFi.localIP().toString().c_str(), PRIVATE);\n    pinMode(led, OUTPUT);\n    timeout = millis();\n}\n\nvoid loop() {\n    char c;\n    long int begin;\n    String line = "";\n    if (millis() <= timeout) {\n        digitalWrite(led, HIGH);\n    } else {\n        digitalWrite(led, LOW);\n    }\n    if (client.connected()) {\n        while (client.available()) {\n            /* get next char */\n            c = client.read();\n            if (\'H\' == c) {\n                server.print("Turn LED on.");\n                timeout = millis() + 5000;\n            } else if (\'L\' == c) {\n                server.print("Turn LED off.");\n                timeout = millis();\n            } else if (\'S\' == c) {\n                if (digitalRead(led)) {\n                    server.print("LED is on.");\n                } else {\n                    server.print("LED is off.");\n                }\n            } else if (\'X\' == c) {\n                server.print("Close client connection.");\n                client.stop();\n            } else {\n                server.write(c);\n            }\n        }\n    } else {\n        /* get next client */\n        client = server.available();\n        if (client.connected()) {\n            server.println("Enter: ");\n            server.println("   H to turn LED on for 5 seconds");\n            server.println("   L to turn LED off");\n            server.println("   S for LED status");\n            server.println("   X to close client connection");\n        }\n    }\n}')


# ### Compiling

# In[12]:


print(particle(["compile", "argon", "--saveTo", "myproject.bin"]).stdout)


# ### Flash firmware

# In[ ]:


print(particle(["flash", device_name, "myproject.bin"]).stdout)


# In[ ]:




