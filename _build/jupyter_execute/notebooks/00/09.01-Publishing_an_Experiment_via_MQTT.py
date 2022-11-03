#!/usr/bin/env python
# coding: utf-8

# # Publishing an Experiment via MQTT
# 
# This notebook is part of a proof concept study regarding use of the Internet of Things (IoT) as infrastructure for engineering teaching laboratories. 
# 
# This notebook uses the [SimPy](https://simpy.readthedocs.io/en/latest/) library a create real-time simulation of a hypothetical experiment. The experiment responds to inputs and publishes data to a remote user via an an MQTT broker. In actual use, the content of this notebook would be implemented in an attached device such as an Arduino, Particle, or Raspberry Pi, with attached sensors.
# 
# The companion notebook ??? demonstrates how a remote client could interact with the experiment via MQTT.

# ## Installations
# 
# The following installations are required for use on Google Colab.

# In[1]:


get_ipython().system('pip install paho-mqtt')
get_ipython().system('pip install simpy')


# ## Publishing a real-time simulation via MQTT
# 
# Topics:
# 
# | topic | messages |
# | :-- | :-- |
# | `cbe-virtual-lab/command` | start and stop experiments |
# | `cbe-virtual-lab/expt-name/data` | topic
# 

# ### Proof of Concept
# 
# Here we experiment with encapsulating the experiment as a standalone class. This is set up so that upon receiving an appropriate message from the remote user, a new instance of the experiment is created and run.

# In[58]:


get_ipython().run_line_magic('matplotlib', 'inline')
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time
import matplotlib.pyplot as plt
import numpy as np
from IPython import display

# select experiment duration

# set up client to interact with cbe-virtual-laboratory

class CBEClient(mqtt.Client):
    
    def __init__(self, recv="", send=""):
        super().__init__()
        self.host = "mqtt.eclipse.org"
        self.recv = recv
        self.send = send

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected: {self.host} with return code {rc}")
        if self.recv:
            self.subscribe(self.recv, qos=2)
            print(f"Subscribed: {self.recv}")
        
    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode("utf-8"))
        print(f"Receieved: {payload} from {self.recv}")
    
    def connect(self):
        super().connect(host=self.host, port=1883, keepalive=60)
        
    def publish(self, payload):
        if self.send:
            super().publish(self.send, payload=payload)
            print(f"Sent: {payload} to {self.send}")
        else:
            print("No send topic has been specified.")
        
    def __enter__(self):
        self.connect()
        self.loop_start()
        time.sleep(0.5)
        print(f"Loop Started: {self}")
        return self
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.loop_stop()
        print(f"Loop Stopped: {self}")
        
def on_message(client, userdata, msg):
    payload = json.loads(msg.payload.decode("utf-8"))
    send = "/".join(["cbe-virtual-laboratory", payload["client_id"]])
    print(send)
    print(f"Message: {payload}")
    with CBEClient(send=send) as expt:
        for k in range(payload["duration"]):
            x = 0
            y = 0
            expt.publish(json.dumps({"time": k, "x" : x, "y" : y}))
            time.sleep(1)

# listen for command on the command channel
with CBEClient(recv = "cbe-virtual-laboratory/command/#") as cbe:
    cbe.on_message = on_message
    time.sleep(30)


# In[ ]:





# ## Version 1
# 
# T

# In[29]:


import time
import simpy
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import json

class Experiment():

    def __init__(self, topic, duration):
        self.topic = topic
        self.duration = duration
        self.env = simpy.rt.RealtimeEnvironment(factor=1)
        self.proc = self.env.process(self.process())
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        self.client.subscribe(self.topic)

    def on_publish(self, client, userdata, result):
        print(f"{client} published with result code {result}")

    def process(self):
        t_start = time.perf_counter()
        t = 0
        y = 2.0
        while True:
            msg = f"{round(t,2)},{y:5.2f}"
            self.client.publish(self.topic, msg)
            yield self.env.timeout(1 - (t - round(t, 0)))
            t = time.perf_counter() - t_start
            y -= 0.1*y

    def run(self, client):
        print(f"Experiment started by {client}")
        self.client.connect("mqtt.eclipse.org", 1883, 60)
        self.env.run(until=self.duration)
        self.client.disconnect()
        print("End experiment.")

# set up client to wait for messages on 
#     cbe-virtual-laboratory/command/#
# expect a message with a specified experiment duration

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("cbe-virtual-laboratory/command/#")

def on_message(client, userdata, msg):
    print(f"Received {msg.payload} from {msg.topic}")
    data = json.loads(msg.payload.decode("utf-8"))
    duration = data['duration']
    expt = Experiment("cbe-virtual-laboratory/expt", duration)
    expt.run(client)

# setup client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# connect client to broker
client.connect("mqtt.eclipse.org", 1883, 60)

# start a non-blocking thread to wait for messages
client.loop_start()

# prove the loop is non-blocking
for k in range(20):
    print(k)
    time.sleep(1)

# don't leave a zombie thread behind
client.loop_stop()


# In[ ]:




