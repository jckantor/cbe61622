#!/usr/bin/env python
# coding: utf-8

# # Setting up the Raspberry Pi for Lab Use

# ## Setup Procedures

# ### Step 0. Learn some Simple Linux Commands
# 
# The Raspberry Pi OS is a version of Linux maintained by the Raspberry Pi Foundation for use on the systems they produce. [Linux](https://en.wikipedia.org/wiki/Linux) is open-source family of Unix-like operating systems that has been ported to a wide variety of systems, ranging from Android phones, personal computers, on up to large server clusters.  
# 
# Linux systems share a common set of simple commands that can be run from a terminal window. While these commands may seem terse and cryptic at first, if you learn to use them you will find them to be quick, powerful productivity tools. The following steps, for example, make use of these commands to set up a Raspberry Pi for use. If you are not already familiar the basic Linux commands, a short summary of the most useful commands is [Basic Linux Commands for Beginners](https://maker.pro/linux/tutorial/basic-linux-commands-for-beginners).

# ### Step 1. Create an OS Image
# 
# The download and imaging of the microSD card takes a while, up to an hour or two. So start this step and let it proceed while you move on to other things.
# 
# 1. Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your laptop.
# 2. Mount the microSD card onto your laptop (typically using a USB microSD card reader).
# 3. Select a Raspberry Pi OS and write the image to the microSD card. 

# ### Step 2. Assemble Case Hardware

# ### Step 3. Initial Configuration
# 
# The initial bootup sequence will include a number of configuration steps. You will need to attach a USB keyboard and mouse to complete these steps.
# 
# * Country: United States
# * Language: American English
# * Timezone: Eastern
# * Check "Use English Language"
# * Check "Use US keyboard"
# 
# The default user is "pi".  We will provide you with a class specific password to use with these devices.
# 
# If the setup process doesn't successfully connect to the local wifi, skip those steps. After the boot process is complete, you can try to connect to wifi again through the taskbar.

# ### Step 4. Update Installed Packages
# 
# It's important to keep your device updated with the latest release of software updates. Open a terminal window and update all installed packages.
# 
#     sudo apt update
#     sudo apt full-upgrade
#     sudo reboot
#     sudo apt autoremove
#     sudo apt clean
#     
#  

# ## Step 5. Configure Options
# 
# In a terminal window, run the command
# 
#     sudo raspi-config
#     
# Options to change:
# 
# * Display Options
#     * D5: Set VNC resolution to 1024x768 or higher
# * Interface Options
#     * P1: Enable RPI camera
#     * P2: Enable SSH
#     * P3: Enable VNC
#     * Consider enabling other options as needed for laboratory interfacing
# * Performance Options
#     * P2: Increase GPU memory to 256 MB
#     
# Reboot when finished.

# ### Step 6. SSH Connectivity
# 
# Remote connection from your laptop to a Raspberry Pi if often useful. To proceed you will need to be on the same network, and need the IP address of the Raspberry Pi.  You can find the IP address from the VNC icon on the task bar, or typing ``hostname -I`` in a terminal window, or by executing ``ping -c 1 raspberrypi`` on the remote device.
# 
# For SSH connection, open a terminal window on your laptop and use the following command
# 
#     ssh pi@xxx.xxx.xxx.xxx
#     
# This should open a terminal window to your Raspberry Pi.  

# ### Step 7. VNC Connectivity
# 
# VNC provides remote access to the full desktop of the Raspberry Pi. If you haven't already done so, install [RealVNC Viewer](https://www.realvnc.com/en/connect/download/viewer/) on your laptop. 
# 
# You will need to know the IP address for the Raspberry Pi. This available by opening the VNC Viewer on the Raspberry Pi, or by executing ``hostname -I`` in a terminal window on the Raspberry Pi, or by executing ``ping -c 1 raspberrypi`` on the remote device.
# 
# Then open a terminal window and setup an additional vncserver with the command
# 
#     vncserver -geometry 1600x900
#     
# using whatever resolution may be appropriate for your laptop. The command will return a new IP/port address you can use to open an additional desktop window to the Raspberry Pi.
# 
# At this stage you may find it convenient to operate the Raspberry Pi in `headless' mode.

# ### Step 8. Other Software Installations

# #### WaveForms (Digilent)
# 
# Use the Raspberry Pi web browser to download and install the ADEPT runtime and WaveForms application.

# #### Python Libraries
# 
# The default distribution of Raspberry Pi OS includes the core Python libraries that are used for many routine calculations, including Numpy, SciPy, and Matplotlib. These libraries, however, do not take full advantage of the Raspberry Pi's multiple cores or the [NEON SIMD unit](https://tttapa.github.io/Pages/Raspberry-Pi/NEON/index.html) incorporated into modern versions of the device. The following installs remove the default libraries, installs a modern BLAS to use the available hardware, and reinstalls core libraries with versions that can use the BLAS.
# 
#     sudo apt remove python3-numpy
#     sudo apt-get install libopenblas-dev
#     sudo apt-get install python3-numpy
#     sudo apt-get install python3-matplotlib
#     sudo apt-get install python3-scipy
#     
# Image processing
# 
#     sudo apt-get install python3-opencv
#     
# Qt Windowing
#    
#     sudo apt-get install python3-pyqt5
#   

# #### [ImageJ](https://imagej.net/platforms/pi) (Not working!)
# 
# The following commands were an attempt to install ImageJ. Unfortunately, the resulting application is, at best, unresponsive and difficult to use. More work will be needed to produce a useable installation.
#     
#     sudo apt-get install openjdk-8-jre
#     sudo update-alternatives --config java
#     java -version
#     cd Downloads
#     wget downloads.imagej.net/fiji/latest/fiji-nojre.zip
#     unzip fiji-nojre.zip
#     wget raw.githubusercontent.com/imagej/imagej2/master/bin/ImageJ.sh

# ### JupyterHub and JupyterLab
# 
# JupyterHub provides a JupyterLab environment that can be accessed locally or remotely through a web browswer. JupyterHub provides a notebook server for every user, a IPython console, and a terminal window. JupyterLab adds additional functionality corresponding to the latest notebook IDE. Together, these package provide a remarkably useful tool for accessing Raspberry Pi devices.
# 
# The following installation instructions are adapted from https://towardsdatascience.com/setup-your-home-jupyterhub-on-a-raspberry-pi-7ad32e20eed for the latest version of Raspberry Pi OS (Bulleye).
# 
# 
# #### Step 1. Verify Python 3 is the default version Python.
# 
# Verify that you have Python 3 installed as the default version of Python
# 
#     python --version
#     
# If this is reporting a version earlier than Python 3, then go no further without first upgrading the OS to the current version of Raspberry Pi OS, Bullseye or later.
# 
# #### Step 2. Install packages
# 
# The next three commands install the services necessary to provide the JupyterHub service, and jupyterhub itself.
# 
#     sudo apt-get install npm 
#     sudo npm install -g configurable-http-proxy
#     sudo -H pip3 install notebook jupyterhub
#     
# #### Step 3. Setup the configuration file for JupyterHub
# 
# JupyterHub requires a configuration file. This step creates a configuration file, makes changes to the file, then moves the file to the root directory so that it can be accessed by all users.  First, be sure we're working in our own home directory.
# 
#     cd ~
#     
# Next, create the configuration file ``jupyterhub_config.py`` in the home directory.
# 
#     jupyterhub --generate-config
#     
# Two changes to this file will adapt its use for the Raspberry Pi. The first is to change the default port from 8000 to 8888 which is more commmonly used for JupyterHub services. Open the file ``jupyterhub_config.py`` using a text editor of your choice (for example, Thonny or nano on the Raspberry Pi). 
# 
#     nano jupyterhub_config.py
#     
# Search for a comment line containing ``# c.JupyterHub.bind_url = 'http://:8000'``. Change the line to read
# 
#     c.JupyterHub.bind_url = 'http://:8888'
#     
# to enable use of the port 8888. To support JupyterLab, search for a comment line containing ``# c.Spawner.default_url = '/user/:username/lab'``. Change the line to read
# 
#     c.Spawner.default_url = '/lab'
# 
# then save the file. Next, move the file to the root directory
# 
#     sudo mv jupyter_config.py /root
#     
# That completes setup and installation of the JupyterHub configuration file.
#     
# #### Step 4. Setup and start JupyterHub as a service.
# 
# Create the jupyterhub.service file, and open for editing
# 
#     sudo touch /lib/systemd/system/jupyterhub.service
#     sudo nano /lib/systemd/system/jupyterhub.service
# 
# Add the following lines, write, and close the file.
# 
#     [Unit] 
#     Description=JupyterHub Service 
#     After=multi-user.target
#     
#     [Service] 
#     User=root 
#     ExecStart=/usr/local/bin/jupyterhub --config=/root/jupyterhub_config.py 
#     Restart=on-failure
#     
#     [Install] 
#     WantedBy=multi-user.target
# 
# Next start the service and setup to restart on reboot
# 
#     sudo systemctl daemon-reload 
#     sudo systemctl start jupyterhub 
#     sudo systemctl enable jupyterhub 
#     
# Confirm the JupyterHub service is active
# 
#     sudo systemctl status jupyterhub.service
# 
# 
# #### Step 5. Setup JupyterLab
# 
#     sudo -H pip3 install jupyterlab  
#     sudo jupyter serverextension enable --py jupyterlab --system
#     
#     
# #### Step 6. Test
# 
# On Chromium browswer on Raspberry Pi, start a JupyterLab session with the link
# 
# ``http://localhost:8888``
# 
# From a remote web server, first verify that the Raspberry Pi can be located on the same network. In a terminal window, ``ping -c 1 raspberrypi`` to locate the IP address. Given the IP address, start a JupyterLab session ``http://xxx.xxx.xxx.xxx:8888``.
# 
# Alternatively, a remote session can be started in a VNC session, then executing
# 
#     jupyter lab
#     
# in a terminal window.

# In[ ]:




