#!/usr/bin/env python
# coding: utf-8

# # Workstation Learning Exercises

# ## Understanding PWM
# 
# 1. Using the pins on an MCU, use the oscilloscope to observe PWM signals and how they respond to Python commands.
# 
# 2. Attach a servo, and observe the response of the servo to a PWM command.

# ## Characterizing noise in a MEMS device.
# 
# Accelerometers are MEMS devices with inherent noise characteristics. This exercise explores the noise characteristics of this device. The learning goals are to understand typical types of noise encountered in sensors.
# 
# Mount the ADXL327 3-axis accelerometer on ADS breadboard. Apply 3.3v power supply and ground. Using the datasheet, select capacitors to provide maximum bandwidth on each axis. Using the spectrum analyzer, identify the noise characteristics of the sensor. 
# 
# Assume for each axis,
# 
# $$a_x = \bar{a_x} + e_x$$
# $$a_y = \bar{a_y} + e_y$$
# $$a_z = \bar{a_z} + e_z$$
# 
# What is frequency spectrum for $e_x$, $e_y$, and $e_z$? Are we seeing 1/f noise, broadband noise, 

# In[ ]:




