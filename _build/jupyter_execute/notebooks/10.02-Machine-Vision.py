#!/usr/bin/env python
# coding: utf-8

# # Machine Vision Applications
# 
# Examples of Machine Vision Requirements
# 
# * Visualize droplets ranging in size from 10 to 100 microns.
# * Visualize a field with 1 million drops
# * Classify 10 micron particles
# 
# Questions
# 
# * Are the particles in motion?
# * How much time is available to capture the image?
# * Do we need a CFA or could a monochrome camera with filters be used?
# * Depth of field? Are the particles in a plane?
# * How are the illuminated?
# * What working distances?
# * Any mounting or geometrical constraints?

# In[22]:


import math

d = 0.05 # mm
object_area = d*d*1000000
print("Field size =", object_area, "mm**2")
print("Field width = ", math.sqrt(object_area), "mm")


# ## Lenses

# ### Fixed focal length lenses
# 
# * [Arducam](https://www.arducam.com/best-m12-c-cs-mount-lenses/)
# * [Raspberry Pi 16mm](https://www.adafruit.com/product/4562)
# 
# A 16mm lens on a 2/3" sensor has a 30 degree angle of view, and a typical minimum object distance of 20cm which is an object field about 11cm in diameter. This is too large for the application.
# 
# ![](https://cdn-shop.adafruit.com/970x728/4562-00.jpg)
# 
# A 2/3" sensor has a diagonal of 7.85mm. An object field of 2cm corresponds to a magnification of 0.4x. A magnification range of 1.0x to 0.3x would seem about right.

# ### Macro and Variable Magnification Lenses
# 
# * [Edmund Infiniprobe 0-3.2x](https://www.edmundoptics.com/p/infiniprobe-s-32-video-microscope-0-32x/15606/)
# 
# 

# ### Telecentric Lenses
# 
# Tutorials and general information:
# 
# * [EO Imaging Lab 2.2: Telecentricity](https://www.youtube.com/watch?v=O-NeZcmYyJ4&ab_channel=EdmundOptics) Edmund Optics video explaining telecentricity and applications to machine vision.
# * [Thorlabs Tutorial](https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=10762)
# 
# Illumination:
# 
# Sources:
# 
# * [Edmund Optical](https://www.edmundoptics.com/c/telecentric-lenses/1003/)
# * [B&H](https://www.bhphotovideo.com/c/buy/telecentric-lenses/ci/34857/N/3564657627)
# 
# 
# Sample Calculations

# In[16]:


import numpy as np
import math

# Sony IMX477 sensor

pixel_size = 1.55  # microns
h_pixels = 4056.
v_pixels = 3040.

h_mm = h_pixels*pixel_size/1000.
v_mm = v_pixels*pixel_size/1000.
d_mm = round(math.sqrt(h_mm**2 + v_mm**2), 3)

print(h_mm, v_mm, d_mm)

# Field of View

h_fov = 15.0 
v_fov = (v_pixels/h_pixels)*h_fov
d_fov = round(math.sqrt(h_fov**2 + v_fov**2), 3)

print(h_fov, v_fov, d_fov)

# magnification
mag =  round(d_mm/d_fov, 2)
print(mag)


# * https://www.edmundoptics.com/p/05x-23-c-mount-platinumtltrade-telecentric-lens/17562/
# 
# ![](https://productimages.edmundoptics.com/3613.jpg?w=225&quality=100&ver=637710189070260316)
# 
# 33.5mm tube diameter
# 50.0mm max external diameter

# ## Sensing Design

# ### Raspberry Pi HQ Camera (Sony IMX477)
# 
# * [Waveshare](https://www.waveshare.com/raspberry-pi-hq-camera.htm)
# 
# ![Technical Drawing](https://www.waveshare.com/img/devkit/accBoard/Raspberry-Pi-HQ-Camera/Raspberry-Pi-HQ-Camera-details-15.jpg)

# ### 30mm Optical Cage
# 
# * [Thor Labs 30mm Cage Components](https://www.thorlabs.com/navigation.cfm?guide_id=2004)
# 
# 3D Printed Mounting plates
# 
# * https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=2273#2869
# * https://www.thorlabs.com/thorproduct.cfm?partnumber=CBB1
# 

# ### Arducam  
# 
# * [Sony IMX477](https://www.arducam.com/product-category/cameras-for-raspberrypi/raspberry-pi-camera-raspistill-raspvivid/raspberry-pi-high-quality-12mp-imx477-camera/) based camera modules.

# ### Picamera

# In[ ]:




