#!/usr/bin/env python
# coding: utf-8

# # Getting Image Data
# 
# The goal of this notebook is to develop a python class for the purpose of counting and labeling flourescent particles captured in images from a prototype for a low-cost medical diagnostic device. 
# 
# In this notebook we'll consider traditional image processing techniques .. i.e., those that directly operate on an image to extract scientific information without resort to machine learning techniques. We'll save that imoportant discussion for another time.

# ##  Books and References
# 
# **Computer Vision Textbooks**
# 
# Nixon, Mark, and Alberto Aguado. Feature extraction and image processing for computer vision. Academic press, 2019. [link](https://www.elsevier.com/books/feature-extraction-and-image-processing-for-computer-vision/nixon/978-0-12-814976-8?countrycode=US&format=print&utm_source=google_ads&utm_medium=paid_search&utm_campaign=usashoppinglr&gclid=Cj0KCQiA7oyNBhDiARIsADtGRZYaMYLGnWyLuobOVDBjKabaFfe8nSTA5m2zmH0BYBN_AFdnKwpU_jkaArGkEALw_wcB&gclsrc=aw.ds)
# 
# Szeliski, Richard. Computer vision: algorithms and applications. Springer Science & Business Media, 2010. [[Hesburgh Library](https://link-springer-com.proxy.library.nd.edu/book/10.1007%2F978-1-84882-935-0)][[Szeliski Web Page and Materials](https://szeliski.org/Book/)][[Preprint of 2nd Edition](https://www.dropbox.com/s/8bf4feleifhrvl6/SzeliskiBookDraft_20210930.pdf?dl=0)]
# 
# **Programming Books**
# 
# Howse, Joseph, and Joe Minichino. Learning OpenCV 4 Computer Vision with Python 3: Get to grips with tools, techniques, and algorithms for computer vision and machine learning. Packt Publishing Ltd, 2020.
# 
# Villán, Alberto Fernández. Mastering OpenCV 4 with Python: A practical guide covering topics from image processing, augmented reality to deep learning with OpenCV 4 and Python 3.7. Packt Publishing Ltd, 2019.
# 
# Pajankar, Ashwin. Raspberry Pi Computer Vision Programming: Design and implement computer vision applications with Raspberry Pi, OpenCV, and Python 3. Packt Publishing Ltd, 2020. [Amazon](https://www.amazon.com/Raspberry-Computer-Vision-Programming-applications/dp/1800207212)
# 
# **Papers**
# 
# Coelho, L.P. 2013. Mahotas: Open source software for scriptable computer vision. Journal of Open Research Software 1(1):e3, DOI: http://dx.doi.org/10.5334/jors.ac
# 
# Van Noorden, Richard. "Publishers launch joint effort to tackle altered images in research papers." Nature (2020). https://doi.org/10.1038/d41586-020-01410-9
# 
# **Blogs and Postings**
# 
# * [Introduction to Computer Vision Using OpenCV and the Raspberry Pi](https://www.circuitbasics.com/introduction-to-computer-vision-using-opencv-and-raspberry-pi/)
# 
# **Digital Camera Sensors for Spectrophotometry**
# 
# Digital camera sensors commonly employ a color filter array to replicate the 
# 
# * Solli, Martin, et al. "Digital camera characterization for color measurements." Proceedings of 2005 Beijing International Conference on Imaging: Technology and Applications for the 21st Century. Beijing (China). 2005. 
# 
# * Solli, Martin. Filter characterization in digital cameras. Institutionen för teknik och naturvetenskap, 2004. [pdf](https://www.diva-portal.org/smash/get/diva2:20007/fulltext01.pdf)
# 
# * Imai, Francisco H., and Roy S. Berns. "Spectral estimation using trichromatic digital cameras." Proceedings of the International Symposium on Multispectral Imaging and Color Reproduction for Digital Archives. Vol. 42. Chiba University Chiba, Japan, 1999. [pdf](http://www.rit-mcsl.org/Lippman2000/Spectral/TechnicalPapers/SpecEstimRGBCamera_Chiba99.pdf)
# 
# * Westland, Stephen, Caterina Ripamonti, and Vien Cheung. Computational colour science using MATLAB. John Wiley & Sons, 2012.
# 
# 

# ## Python Packages for Computer Vision
# 
# See https://www.analyticsvidhya.com/blog/2021/04/top-python-libraries-for-image-processing-in-2021/ for a survey of Python libraries for image processing.
# 
# **Standard Python Libaries**
# 
# One of the very nice aspects of image processing with Python is the wide adoption of basic NumPy arrays to represent image data. This facilitates the use of methods from multiple packages for a particular project.
# 
# * [NumPy]() NumPy provides the basic multi-dimensional array data structure used by other image processing libraries.
# 
# * [Matplotlib]() Matplotlib incudes functions to read image files in several common formats, and display images.
# 
# * [scipy.ndimage](https://docs.scipy.org/doc/scipy/tutorial/ndimage.html) SciPy provides a useful collection of image processing algorithms. 
# 
# * [scikit-image](https://scikit-image.org/) A library designed to interoperate with NumPy and SciPy.ndimage libraries.
# 
# **Pure Python Libraries**
# 
# * [Pillow](https://pillow.readthedocs.io/en/stable/) A fork of the original Python image library (PIL), Pillow is one of the most important Python libraries for image processing, and the foundation for many other packages. For x86 architectures, [Pillow-SIMD](https://github.com/uploadcare/pillow-simd) is a fork that "follows" Pillow to provide algorithms tuned to the x86 SIMD hardware.
# 
# * [Imageio](https://github.com/imageio/imageio) Imageio is a cross-platform, pure Python library to read and write images, video, volumetric data, and scientific formats. This is a good, lightweight choice if the reading and writing files in multiple formats is the primary purpose.
# 
# **Full Featured Computer Vision Packages**
# 
# * [OpenCV/cv2](https://opencv.org/) OpenCV is a C++ library  launched in 1999 at Intel Research to advance real-time computer vision. In 2011 is was taken over by the non-profit foundation OpenCV.org. OpenCV is widely used with mulitple language bindings, full ecosystem of third party documentation, training courses, and [books](https://opencv.org/books/). The Python bindings are accessed by importing the cv2 Python module.
# 
# * [Mahotas](https://mahotas.readthedocs.io/en/latest/) A computer vision library written in Python and CPython. While OpenCV is the fastest package, the lack of type checking can result in hard crashes. Mahotas includes type checking with some loss of speed. A paper describing the package is available http://doi.org/10.5334/jors.ac.
# 
# * [SimpleITK]() The Natonal Library of Medicine Insight Segmentation and Registration Toolkit (ITK). [book](https://itk.org/ItkSoftwareGuide.pdf)
# 
# **Photo Conversion and Management Tools**
# 
# * [ImageMagick](https://imagemagick.org) ImageMagick is a widely-used, full-featured package  to create, edit, compose, and convert images. It is available on all major platforms including the Raspberry Pi OS. [Wand](https://pypi.org/project/Wand/) is a Python binding to the ImageMagick API. See https://www.pythonpool.com/imagemagick-python/ for information using Wand and ImageMagick.
# 
# * [XnView MP](https://www.xnview.com/en/xnviewmp/) A commercial digital asset management tool available on Windows, Mac OS, and Linux. There are many alternatives on the market.
# 
# **Outdated or deprecated libraries** 
# 
# These are included here so you know what not to use for your projects.
# 
# * [cImage](https://github.com/bnmnetp/cImage) A simple image processing library for Python. Intended for use in introductory computer science courses. Uses PIL.
# 
# * [PIL]() Python image library. Hasn't been updated since 2009, now outdated and insecure. Largely been replaced by Pillow, a friendly fork of PIL.
# 
# * [SimpleCV](http://simplecv.org/) An open source Python library based on OpenCV designed for rapid development of cmputer vision applications, with accompanying book from Reilly Media. There's no evidence of continued development, and not compatible with recent versions of Python 3.

# ### File Formats
# 
# For this case study we will be developing techniques to analyze images stored as computer files. Later we may consider applying these techniques to a live video stream, but for now we'll use stored images.
# 
# Things to know about image files.
# 
# * *Raster* versus *vector* images. Image sensors produce raster images.
# 
# 
# * Image files can get large, and are often stored in some sort of compressed form.
#     * No compression -- not commonly encountered since lossless compression is so straightfforward.
#     * Lossless compression -- techniques to encode the data using fewer characters. The most common method of storing raw image data.
#     * Lossy compression -- willing to sacrifice some image detail for significantly reduced storage requirements. This technology enables jpeg, mpeg, and video streaming protcols.
# 
# 
# * The suffix of an image file usually (i.e., no guarantee) indicates the image file format. 
#     * .svg, .dxf, .eps, .pdf -- Vector "document" files which can contain multiple elements in addition to the vector graphics. SVG (scalable vector graphics) is supported by most browsers
#     * .png -- The most frequently used losslessly compressed raster image file format widely supported by web browsers. Unlike .jpg, .png allows a transparency channel.  It has largely replaces GIF (Graphics Interchange Format) which is now used primarily for simple animations. 
#     * .tiff/.tif -- Tagged Image File Format was introduced to support cross-platform photo editing. Note that .tif files may encode lossy image formats.
#     * .dng, .raw, and other raw formats -- Formats that encode the data directly sampled from the image sensor. Useful for post-processing images, and re-processing images.
#     * .jpeg/.jpg -- perhaps the most common standard for image files. This is a lossy format, and can be very lossy in extreme cases.
#     
# General recommendations for scientific use.
# 
# * Use lossless image formats when possible. Store the original as a master file. Use a file naming convention to track derivatives of the original image.
# * Use .png for line art, graphics, especially for web use.
# * Use high quality .jpg for photographs and realistic images. Be careful with "generational loss". Always use sRGB color space which is, by far, the most common color space used for .jpg files.
# * When possible lossless .tif, .dng, and raw formats to capture and archive original image data. 

# ## Image Metadata
# 
# Image files also carry *meta-data* providing additional information about the image. There several different standards for meta data, the most common being *exif* data embedded in the image file, or a companion *.xmp* file hold data in the [Extensible Image File Format](https://en.wikipedia.org/wiki/Exif)  Metadata Platform format. **exiftool** is a command line tool included with many operating systems.
# 
# [Description of Exif file format](https://www.media.mit.edu/pia/Research/deepview/exif.html)

# In[36]:


import glob
from PIL import Image
from PIL.ExifTags import TAGS

# print list of all files in a directory
path = "./image_data/Jiang Photos/"
files = glob.glob(path + '*')
for file in files:
    print(file)
    
# get all files in directory
for file in glob.glob(path + '*'):
    
    # display thumbnail 
    im_thumb = Image.open(file)
    im_thumb.thumbnail((100, 100))
    print(f"\n{file}")
    display(im_thumb)
    
    im = Image.open(file)
    exifdata = im.getexif()
    for tag in exifdata.keys():
        print(TAGS.get(tag), end=": ")
        print(exifdata[tag])


# ## More Examples of Image Metadata

# In[42]:


im = Image.open("image_data/25-miniM.tif")
exifdata = im.getexif()
for tag in exifdata.keys():
    print(TAGS.get(tag), end=": ")
    print(exifdata[tag])


# In[43]:


get_ipython().system('/usr/local/bin/exiftool image_data/25-miniM.tif')


# What's not present in this example?  (Hint: What colors are being displayed?)
# 
# Here's the exif data for a photograph prepared through a typical photographer's workflow: RAW --> Noise Reduction --> Adobe Lightroom --> .jpg for export. Carefully look for the color space data.

# In[45]:


im = Image.open("image_data/eagles-photo-low-quality.jpg")
exifdata = im.getexif()
for tag in exifdata.keys():
    print(TAGS.get(tag), end=": ")
    print(exifdata[tag])

print()
get_ipython().system('/usr/local/bin/exiftool image_data/eagles-photo-low-quality.jpg')


# ### Calibrating Monitors
# 
# Accurate color reproduction requires color management from source to display. At each Color management is now a standard part of most operating systems 

# In[ ]:




