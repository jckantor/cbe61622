#!/usr/bin/env python
# coding: utf-8

# # Installing an Image Processing Toolkit on Raspberry Pi
# 
# The purpose of this notebook is to outline a workflow and toolkit for capturing and processing images forlaboratory use on the Raspberry Pi. There are, of course, a nearly limitless collection of tools that can be adapted for laboratory use, and numerous specialized software packages. The particular workflow desecribed below is oriented to the use of Jupyter notebooks to document the analysis of images, and the use of the most common image libraries in Python.
# 
# 1. Installing Jupyter Notebook
#     * Miniconda
#     
# 2. Image Capture
#     * PiCamera 2
#     
# 3. Image Processing Libraries
#     * PIL
#     * scipy ndimage
#     * OpenCV
#     * scikit-image
#     
# 4. ML Libraries
#     * tensorflow
#     * scikit-learn
#     
#     

# ## 1. Installing Miniconda on Raspberry Pi (64 bit)
# 
# ### Download and Installation
# 
# Anaconda is a big package with a comprehensive set of Python libraries and application utilities. Miniconda is a smaller alternative that relies on user intervention for downloading needed libraries and applications. 
# 
# Go to this page for a version of Miniconda that works with RaspOS: https://github.com/conda-forge/miniforge. Download the version labeld "aarch64 (arm64)". This is a large download and may take many minutes to complete.
# 
# After the download is complete, open an terminal window, navigate to the Downloads directory, and execute the shell script.
# 
#     ls Downloads
#     sh Miniforge3-Linux-aarch64.sh
#     
# A new folder `miniforge3` will appear in the home directory. This is a long process requiring you to respond to various prompts. When complete, close and reopen the terminal window. If all went well, then command line
# 
#      conda
# 
# should return a help message. Executing
# 
#     conda update conda 
#     
# will bring the conda environment up to date.
#     
#     
# ### Install Jupyter
# 
# To install Jupyter, execute
# 
#     conda install jupyter
# 
# You can test the Jupyter environment on the Raspberry Pi with 
# 
#     jupyter lab
#     
# You may be asked for your password. 
# 
# ### Accessing Jupyter Remotely
# 
# One of the excellent features of Miniconda is that you can access the Jupyter server remotely. That is, you can be doing your typing, coding, and analysis remotely on your laptop while the Raspberry Pi server remains attached to your laboratory equipment. The following steps are adapted from https://towardsdatascience.com/remote-computing-with-jupyter-notebooks-5b2860f761e8
# 
# 1. Confirm your laptop is on the same network.
# 
# 2. On your laptop, open a terminal or command window use ping to locate the Raspberry Pi. Note the IP address which will be in the form XXX.XXX.XXX.XXX
# 
#         ping raspberrypi
#         
# 3. From the laptop, open an `ssh` session. Follow prompts to login to the Raspberry Pi.
# 
#         ssh username@XXX.XXX.XXX.XXX
#         
# 4. Open a jupyter session 
# 
#         jupyter lab --no-browser 
#         
# 5. Redirect port traffic from the Raspberry Pi. Open another terminal or command window, and issue the command. Answer any prompts that may appear.
# 
#         ssh -N -L localhost:8890:localhost:8889 username@XXX.XXX.XXX.XXX
#         
# 6. Finally, open a browser window on your laptop and open the following web address. You should now have a Jupyter lab session that is connected to the Raspberry Pi.
# 
#         localhost:8890/lab
#         
# From this point on you should be be able to use to the Raspberry Pi remotely.

# ## Image Capture
# 
# Image capture refers to the capture of images using a connected camera. The workflow begins with the

# ### Installing PiCamera2
# 
#     sudo apt install -y python3-picamera2

# In[1]:


get_ipython().system('sudo apt install -y python3-picamera2')


# ### Capturing Images
# 
# We will assume you have a compatible camera connected to the Raspberry Pi using the standard ribbon cables. 

# #### Camera Setup
# 
# The `libcamera` utilities a good place to get started with use of the Raspberry Pi camera system.  From a terminal window on the Raspberry Pi, issue the following command
# 
#         libcamera-hello -t 0
#         
# to open a realtime preview from the camera. Use this as an opportunity to frame the scene, adjust lighting, focus the lens if necessary. Close the preview window when finished.

# #### Capture a jpeg with libcamera-jpeg
# 
# The simplest way to capture an image is using `libcamera-jpeg`. For a list of all options execute
# 
#         !libcamera-jpeg --help
#         
# from a cell in a Jupyter notebook. A typical use of is shown in the next cell.

# In[4]:


get_ipython().system('libcamera-jpeg -o test.jpeg')


# In[2]:


get_ipython().system('ls')


# In[5]:


import matplotlib.pyplot as plt

img = plt.imread("test.jpeg")
plt.imshow(img)


# #### Capture an Image with Picamera
# 
# A common use case is using a Python script to capture an image.

# In[8]:


from picamera2 import Picamera2, Preview
import time

picam2 = Picamera2()

camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)})
picam2.configure(camera_config)
picam2.start()
exif = picam2.capture_file("test.jpg")
picam2.close()

for key, val in exif.items():
    print(key, ":", val)


# In[5]:


import matplotlib.pyplot as plt

img = plt.imread("test.jpg")
plt.imshow(img)


# In[9]:


get_ipython().system('mail --help')


# In[ ]:




