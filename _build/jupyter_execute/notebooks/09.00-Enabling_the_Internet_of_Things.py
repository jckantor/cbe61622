#!/usr/bin/env python
# coding: utf-8

# # Enabling the Internet of Things
# 
# MQTT is a lightweight protocol for delivering messages between devices through an intermediate broker. Senders declare a 'topic' and 'publish' messages to the broker. Receivers 'subscribe' to particular topics on the broker to receive a copy of all messages pertaining to that topic. Connections between a device and broker are typically over a TCP/IP network, but other transport mediums are in common use. This robust and flexible 'hub-and-spoke' architecture has been widely adopted for 'Internet of Things' (IoT) applications.
# 
# The MQTT acronym was orginally an abbreviation for Message Queuing Telemetry Transport that was developed by individuals at IBM and Cirrus Link (later Eurotech) for monitoring pipeline by satellite in remote locations. IBM later submitted the protocol to the global standards body, OASIS and ISO, where they are now maintained as open standards.

# ## Background
# 
# Descriptions
# 
# * [MQTT.org](MQTT.org)
# 
# Primers and Tutorials
# 
# * mqtt primer: https://www.youtube.com/watch?v=AxC_ykketIg&ab_channel=wcltalkstech
# * HiveMQ MQTT Essentials: https://www.hivemq.com/tags/mqtt-essentials/
# 
# * [Using MQTT to send and receive data for your next project](https://opensource.com/article/18/6/mqtt)
# 
# MQTT for Process Applications
# 
# * [How MQTT is advancing automation and control](https://www.flowcontrolnetwork.com/process-control-automation/article/21122615/how-mqtt-is-advancing-automation-and-control)
# 
# * [MQTT, open SCADA publish/subscribe protocol is getting what it needs to go industrial](https://www.controlglobal.com/articles/2019/mqtt-open-scada-publishsubscribe-protocol-is-getting-what-it-needs-to-go-industrial/)
# 
# Bidirectional Messaging
# 
# * [Two Way communication Using MQTT and Python](http://www.steves-internet-guide.com/two-way-communication-mqtt-python/)
# 
# 

# ## Implementation for CBE-Virtual-Laboratory

# For the purposes of the CBE-Virtual-Laboratory, we propose a topic naming scheme that will enable bidirectional communication between devices, and provide for the setup and tear down of applications and connections.  
# 
# * The highest level to the topic is assigned `cbe-virtual-laboratory`.  
# * The second level designates the laboratory application. This may consist of one or more topic strings designating, for example, a location and application.
# * The third level designates a device
# * The fourth level designates a channel
#     * command
#     * send
#     * receive
#     
#    
# 
# 
#     cbe-virtual-laboratory/APPLICATION/DEVICE/CHANNEL

# ## Useful Apps and Links
# 
# * **MQTTBox** A Windows/Linux/Mac App to create MTQQ clients and monitor the broker.
# * [Reporting temperature using our Particle Argon through MQTT and the TICK stack](https://www.youtube.com/watch?v=AxC_ykketIg&ab_channel=wcltalkstech)

# In[ ]:




