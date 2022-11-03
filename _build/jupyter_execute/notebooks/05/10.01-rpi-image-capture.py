#!/usr/bin/env python
# coding: utf-8

# # Image Capture
# 
# > Great minds discuss ideas; average minds discuss events; small minds discuss people.
# >
# > *Eleanor Roosevelt*
# 
# Let's get the ideas in order before discussing equipment and processes.
# 
# ![](https://i.pinimg.com/originals/ef/57/92/ef579242f3a4c24fe01d543f04a656b7.jpg)

# ## References
# 
# Main Reference
# 
# * Miikki, K; Karakoc, A. et al. An open-source camera system for experimental measurements, SoftwareX, 2021, 14, 100688 (freely accessible @  https://www.sciencedirect.com/science/article/pii/S2352711021000339#appA) <a href="https://doi.org/10.5281/zenodo.4300692"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.4300692.svg" alt="DOI"></a>  Also see [rpi-camera github repository](https://github.com/kmiikki/rpi-camera).
# 
# Secondary References
# 
# * Wilkes, Thomas C., et al. "Ultraviolet imaging with low cost smartphone sensors: Development and application of a raspberry Pi-based UV camera." Sensors 16.10 (2016): 1649. (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5087437/) [pdf](https://core.ac.uk/download/pdf/46565912.pdf)
# 
# * Deep Ultraviolet Imaging Using the Raspberry Pi HQ Camera [Steropi Blog](https://stereopi.com/blog/deep-ultraviolet-imaging-using-raspberry-pi-hq-camera)
# 
# * Raspberry Pi Documentation: Camera (https://www.raspberrypi.com/documentation/accessories/camera.html)
# 
# * [Giving Linux a Camera Stack: libcamera's 3 Years Journey and Exciting Future](https://youtu.be/r8ByyJzSKG8) (YouTube video)
# 

# ## Light
# 
# Radiometry vs Photometry
# 
# * **Radiometry**: Measuring light in any portion of the electromagnetic spectrum, typically infrared, visible, ultraviolet
# * **Photometry**: Measuring light in units weighted by sensitivity of the human eye.
# 
# SI Units for Photometry
# 
# * Candela (cd): SI unit of luminous intensity
# * Luminous power per unit solid angle emitted by a point light source. 1 cd = 1 lumen/SR
# * 1 candela is approximately equal to light emitted by a common wax candle
# * Luminous intensity is weighted to match human perception.
# 
# More on Lumens, Lux, and Nits: https://www.konicaminolta.com/instruments/knowledge/light/concepts/04.html
# 

# ## Perception
# 
# https://www.olympus-lifescience.com/en/microscope-resource/primer/lightandcolor/humanvisionintro/
# 
# ![](http://hci.cs.siue.edu/NSF/Files/Semester/Week9-2/PPT-Text/images/Image13.png)
#     
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/CIE_1931_Luminosity.png/640px-CIE_1931_Luminosity.png)
# 
# * Human Perception
# 
# https://www.olympus-lifescience.com/en/microscope-resource/primer/lightandcolor/humanvisionintro/
# 
# ![](https://static3.olympus-lifescience.com/data/olympusmicro/primer/lightandcolor/images/humanvisionfigure6.jpg?rev=63C6)
# 
# ![](https://www.ecse.rpi.edu/~schubert/Light-Emitting-Diodes-dot-org/chap16/F16-02%20Photopic%20mesopic%20scotopic%20vision.jpg)
# 
# 
# 
#     
# * Representing images
#     * Gamma
#     * RGB, CYMK, YUV, etc
#     * Color spaces
#     * Color management and calibration
#     * Gamma
#     * Histograms
#     

# ### Color Gamut
# 
# ![](https://upload.wikimedia.org/wikipedia/commons/thumb/6/60/Cie_Chart_with_sRGB_gamut_by_spigget.png/430px-Cie_Chart_with_sRGB_gamut_by_spigget.png)

# ### Lens and Aperture
# 
# #### Etendue
# * Property of light in an optical system
# * Area of the entrance pupil times solid angle the source subtends viewed from the pupil
# * Etendue is like entropy, always increases in an optical system
# 
# #### Simple Lenses
# https://en.wikipedia.org/wiki/Lens
# 
# * Simple lenses
# * Focal length, refraction, and the Lensmaker's equation
# * Real and Virtual image
# * Magnification
# * Abberations
#     
# #### Complex lenses
#     
# * microscopes (https://www.ccmr.cornell.edu/wp-content/uploads/sites/2/2018/03/Reading_-How-do-the-lenses-in-a-microscope-work_.pdf) 
#         ![](https://image1.slideserve.com/2952580/slide8-l.jpg)
# * 4f systems and fourier optics
# * telecentric lenses
# * epi-lighting schemes

# ### Sensor
# 
# ![](https://static.techspot.com/articles-info/850/images/CMOS-j_1100.webp)
# 
# IR/UV/Anti-Aliasing/Microlens/Color Filter Array
# 
# ![](https://www.arducam.com/wp-content/uploads/2020/11/sony-image-sensor-back-illuminated-and-front-illuminated-22.jpg)
# 
# ![](https://static.techspot.com/articles-info/850/images/Module-GS5-S-j_1100.webp)
# 
# * Sensor 2. Electronics
#     * [OV5642 Data Sheet](https://www.uctronics.com/download/cam_module/OV5642DS.pdf)
#     ![](https://www.arducam.com/wp-content/uploads/2019/04/ov5642_diagram.jpg)
#     * [IMX477 Data Sheet](https://www.arducam.com/sony/imx477/)
#     ![](https://www.arducam.com/wp-content/uploads/2020/11/BLOCK-DIAGRAM-1024x564.png)
# 

# ### Camera as a System
# 
# * Feedback
#     * Exposure control
#     * Automatic white balance
#     * Autofocus
#     
# * Equivalence
# 
# ![](https://www.raspberrypi.com/app/uploads/2020/05/Libcamera-Diagrams-01-500x334.jpg)
# 
# ![](https://www.raspberrypi.com/app/uploads/2020/05/Libcamera-Diagrams-02-500x334.jpg)

# ## Software Tools
# 
# * libcamera + qcam
# * OpenCV
# * RawTherapee ``sudo apt-get install rawtherapee``
# * imageio
# * ImageJ

# In[ ]:




