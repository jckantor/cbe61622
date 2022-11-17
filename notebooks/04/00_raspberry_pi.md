# Raspberry Pi

The Raspberry Pi ecosystem provides options for a wide range of laboratory applications. The recommendations given below are designed to get you started with an initial build of a Raspberry Pi to learn what the ecosystem has to offer. More experienced builders may wish to modify these recommendations to better suit specific applications.

## References and Documentation

Overview of the Raspberry Pi in Science applications.

* [Broad-scale applications of the Raspberry Pi: A review and guide for biologists](https://besjournals.onlinelibrary.wiley.com/doi/10.1111/2041-210X.13652)
* [Raspberry Pi computers are helping revolutionize biological research](https://www.britishecologicalsociety.org/raspberry-pi-computers-are-helping-revolutionize-biological-research/)

User guides to getting started with Raspberry Pi.

* [Raspberry Pi Beginner's Guide 4th Edition](https://magpi.raspberrypi.com/books/beginners-guide-4th-ed) A widely used guide intended for a broad audience. Free download available.
* [Raspberry Pi Cookbook: Software and Hardware Problems and Solutions](https://www.amazon.com/Raspberry-Pi-Cookbook-Software-Solutions/dp/1492043222/ref=asc_df_1492043222) A thorough guide to the Raspberry Pi hardware and software.

Representative examples of scientific instruments built using the Raspberry Pi platform. 

* Aidukas, T., Eckert, R., Harvey, A. R., Waller, L., & Konda, P. C. (2019). Low-cost, sub-micron resolution, wide-field computational microscopy using opensource hardware. Scientific reports, 9(1), 1-12. [[pdf](https://www.nature.com/articles/s41598-019-43845-9)]

* Jin, H., Qin, Y., Pan, S., Alam, A. U., Dong, S., Ghosh, R., & Deen, M. J. (2018). Open-source low-cost wireless potentiometric instrument for pH determination experiments. [[pdf](https://pubs.acs.org/doi/pdf/10.1021/acs.jchemed.7b00479)]

* Irving, P., Cecil, R., & Yates, M. Z. (2021). MYSTAT: A compact potentiostat/galvanostat for general electrochemistry measurements. HardwareX, 9, e00163. [[pdf](https://www.sciencedirect.com/science/article/pii/S2468067220300729)]

Many more examples can be found in journals such as [HardwareX](https://www.sciencedirect.com/journal/hardwarex).

## Recommended Hardware

[Princeton Council on Science and Technology](https://cst.princeton.edu/studiolab/equipment/raspberry-pi-kits)

### Core Requirements

The core components of any build is a CPU module, power supply, and micro SD card.

* **Raspberry Pi 4 B (4 or 8 GB preferred)** [[Adafruit](https://www.adafruit.com/product/4564)] [[Amazon](https://www.amazon.com/Raspberry-Model-2019-Quad-Bluetooth/dp/B07TC2BK1X/)] Raspberry Pi boards are in short supply and often sold out.
* **Raspberry Pi Power Supply** [[Vilros](https://vilros.com/products/official-raspberry-pi-foundation-power-supply-for-raspberry-pi-4-us-white-ul)]
* **32GB microSD card preloaded with NOOBS** [[Vilros](https://vilros.com/collections/raspberry-pi-accessories/products/samsung-32-gb-evo-plus-class-10-micro-sd-card-preloaded-with-noobs-micro-sd-usb-adapter)] If you purchase a generic micro SD card you will need to load it with the Raspberry Pi OS. For that purpose will need a [micro SD card adapter](https://www.amazon.com/Technology-Supports-MicroSDXC-MicroSDHC-Midnight/dp/B07YGXR8N3/) for your laptop. 

### Keyboard/Mouse

A Raspberry Pi can be operated in a "headless" mode that uses a laptop for display, keyboard, and mouse/trackpad. But setting up such a system for a first time user can be challenging. It is helpful to have a wired USB connected keyboard and mouse to diagnose set up problems, especially for first time builders.

* **Raspberry Pi Keyboard** [[Vilros](https://vilros.com/products/raspberry-pi-keyboard-and-hub)]
* **Raspberry Pi Mouse** [[Vilros](https://vilros.com/products/official-raspberry-pi-mouse-red-white?variant=26341130666084)]


### Case/Display Options

#### Option 1. HDMI Monitor and Case

The first option is generally the easiest way to set up a Raspberry Pi. What you need is a standard HDMI monitor and cable. The Raspberry Pi can be mounted in a case to sit on the lab bench.

* **HDMI Monitor** There innumerable choices. 
* **micro HDMI to HDMI cable** Note that a micro HDMI to HDMI cable will be required for most monitors.
* **Case** Many options are available. The Argon ONE V2 case offers a well designed aluminum case that provides access via a removable cover to the GPIO pins and a slot for a camera ribbon cable.

#### Option 2. Raspberry Pi Display with Integrated Case
  
* **Raspberry Pi 7" Touch Screen** [[Vilros](https://vilros.com/collections/raspberry-pi-accessories/products/raspberry-pi-7-touchscreen-lcd-display)]
    * Micro HDMI Adapter
    * Micro USB to USB-C adapter
    
* SmartiPi Touch Pro

Follow setup instructions. Use default configurations of Raspbian for user name `pi`. Choose password carefully and keep it on file for use in the laboratory.

## Cameras

* **Raspberry Pi Camera Module V2** [[]()]

* **Raspberry Pi HQ Camera** [[Vilros](https://vilros.com/products/official-raspberry-pi-4-hq-camera)]

* **Arducam IMX519 autofocus camera module for Raspberry Pi** [[Vilros](https://vilros.com/products/arducam-imx519-autofocus-camera-module-for-raspberry-pi?_pos=9&_sid=fe3e9a499&_ss=r)] An autofocus camera module.