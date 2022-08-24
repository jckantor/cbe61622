#!/usr/bin/env python
# coding: utf-8

# # Grove Starter Kit for Raspberry Pi Pico
# 
# * [Grove Starter Kit for Raspberry Pi Pico](https://www.seeedstudio.com/Grove-Starter-Kit-for-Raspberry-Pi-Pico-p-4851.html) with Free Course -- Product Page
# * [Wiki for Grove Starter Kit for Raspberry Pi Pico](https://wiki.seeedstudio.com/Grove_Shield_for_Pi_Pico_V1.0/)
# 

# ## Communication methods
# 
# * **SPI (Serial Peripheral Interface)**.  Developed by Motorola in the 1980's for short distance communication in embedded systems. SPI typically operates at up to a few MHz with a single controller and one or more peripherals. It requires at least four wires and commonly used for SD cards and LCD displays.
# * **I2C (Inter-Integrated Circuit)**. A communication bus invented by Phillips Semiconductors in 1982. The purpose of the bus is to attach peripheral integrated circuits to processors over short distances. Unlike SPI, I2C can have multiple controllers and peripherals on the same bus. It has been widely adopted for embedded systems applications with data transfer requirements below about 400 kbit/second.
# * **UART (Universal Asynchronous Receiver/Transmitter)**. UART describes a physical circuit in a chip or microcontroller to transmit anad receive serial data from a UART located on another device. Only two wires are required in addition to a ground wire, no clock signal in needed. 
# * **PIO (Programmable I/O)**.

# ## I2C Protocol
# 
# I2C refers to Inter-Integrated Circuit, a communication bus invented by Phillips Semiconductors in 1982. The purpose of the bus is to attach peripheral integrated circuits to processors over short distances. It has been widely adopted for embedded systems applications with data transfer requirements below about 400 kbit/second. This is sufficient for many instrumentation requirements.
# 
# The communications bus requires two signal lines designated SDA (data)and SCL (clock). Both are open-collector (or open-drain) lines requiring pull up resistors to maintain a quiescent high state. Typical voltages are +5 or +3.3 volts.
# 
# An I2C bus can have multiple controllers and peripherals. A controller initiates a data transfer, the peripheral responds. A data transfer is performed as follows:
# 
# 1. A controller pulls the SDA line low. The first device on the bus to pull SDA low is the controller. This is the start condition.
# 
# 2. The controller then pulls the SCL line low.

# ## I2C Pinout
# 
# The Raspberry Pi Pico provides two independent I2C channels, numbered 0 and 1, that are accessible through the GPIO pins. The following table shows GPIO pin where I2C channel 0 and I2C channel 1 can be accessed. 
# 
# | I2C0 SDA/SCL | I2C1 SDA/SCL |
# | :--: | :--: |
# | GP0, GP1 | GP2, GP3 |
# | GP4, GP5 | GP6, GP7 |
# | GP8, GP9 | GP10, GP11 | 
# | GP12, GP13 | GP14, GP15 |
# | GP16, GP17 | GP18, GP19 |
# | GP20, GP21 | GP26, GP27 |
# 
# ![](https://microcontrollerslab.com/wp-content/uploads/2021/01/Raspberry-Pi-Pico-pinout-diagram.svg)
