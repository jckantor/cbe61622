#!/usr/bin/env python
# coding: utf-8

# # Operational Amplifiers

# ## Readings

# ## Laboratory Exercises
# 
# ### 1. Familiarization with Operational Amplifiers
# 
# 1. In the Analog Devices ADALP2000 kit, locate
#      * OP27 Low Noise, Precision Operational Amplifier
#      * OP37 Precision Operational Amplifier
#      * OP97 Low Noise, Precision Operational Amplifier
#      * OP482 High Speed JFET Op Amp
#      * OP484 Precision Rail-to-Rail Op Amp
#      * AD8226 Instrumentation Amplifier
#      * AD8542 CMOS Rail-to-Rail Op Amp
#      * ADLT082 JFET Op Amp
#      
# 2. For each Op Amp above, locate (2) data sheet and (2) unit price. For each, write one sentence describing describing what makes that op amp unique from the others. 
# 
# ### 2. Laboratory Testing
# 
# 1. Using the OP27
#     * Setup +/- 12 volt power
#     * Use a 10K potentiometer to create an adjustable voltage divider. Use as the input to the Op-amp according to Fig 8.7 and 8.8 of the text. Can you estimate the gain $A_0$?
#     
#     
# 2. Buffer Circuit (Unity Gain)
# 
# 3. Inverting Amplifier
# 
# 4. Non-inverting Amplifier
# 
# 5. Current-to-Voltage Converter
#     * Locate the phototransistor in the ADALP2000 kit. Locate the data sheet. Set up a current to voltage converter (see Figure 8.41 for ideas) and verify measurement of a light source.
# 
#      
#      
# Ignore this cell.  Just some edit notes(Harvey Mudd) 

![Op](http://fourier.eng.hmc.edu/e84/lectures/figures/OpAmp0.gif)

* [Input impedance]
* [Output impedance]
* [Open-circuit gain]

An approximate equation for the output voltage is

$$V_{out} = A_d (V_+ - V_-) + A_c(V_+ + V_-)$$

where $A_d$ is the differential gain and $A_c$ is the common-mode gain. Normally we seek very high values for $A_d$ and very low values for $A_c$. The common-mode rejection ratio is

$$CMRR = 20 \log_{10}\frac{A_d}{A_c}$$

Typical values of $CCMR$ are 100db or greater indicating $A_d > 10^5A_c$
# ## Feedback

# In[ ]:




