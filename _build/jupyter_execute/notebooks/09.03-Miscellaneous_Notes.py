#!/usr/bin/env python
# coding: utf-8

# # Accessing MQTT Devices

# ## Installing paho-mqtt library

# In[ ]:


get_ipython().system('pip install paho-mqtt')


# ## Particle Argon
# 
# The following code is flashed to the Particle Argon using the Particle Web IDE.
# 
# ```
# // Report temperature and humidity sensor. Provide a short blink of D7
# // to indicate an temperture/humidity update.
# 
# #include <Grove_Temperature_And_Humidity_Sensor.h>
# #include <MQTT.h>
# 
# int led = D7;
# DHT dht(D2);
# 
# float temp, humidity;
# 
# void callback(char* topic, byte* payload, unsigned int length);
# MQTT client("mqtt.eclipse.org", 1883, callback);
# 
# // receive message
# void callback(char* topic, byte* payload, unsigned int length) {
# }
# 
# void setup() {
#     
#     dht.begin();
#     pinMode(led, OUTPUT);
#     client.connect("argon_" + String(Time.now()));
# }
# 
# void loop() {
#     
#     temp = dht.getTempFarenheit();
#     humidity = dht.getHumidity();
#     
#     client.publish("cbe-virtual-laboratory/devices/argon", Time.timeStr() + ", " + String(temp, 1) + ", " + String(humidity, 1));
#     
#     digitalWrite(led, HIGH);
#     delay(200);
#     digitalWrite(led, LOW);
#     delay(4800);
# }
# ```

# ## Receiving data from Particle Argon device

# In[ ]:


import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import time

# select experiment duration
broker = "mqtt.eclipse.org"
topic = "cbe-virtual-laboratory/devices/#"
duration = 30

# callback after completing connection
def on_connect(client, userdata, flags, rc):
    print(f"Connected to {broker} with result code {rc}")
    client.subscribe(topic)

# callback after receiving a message
def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode('utf-8')}")

# create and setup MQTT client
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, 1883, 60)

# listen for measurement information
client.loop_start()
time.sleep(duration)
client.loop_stop()


# In[ ]:




