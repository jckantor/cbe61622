#!/usr/bin/env python
# coding: utf-8

# # Operational Amplifiers

# (Harvey Mudd) ![](http://fourier.eng.hmc.edu/e84/lectures/figures/OpAmp0.gif)
# 
# * [Input impedance]
# * [Output impedance]
# * [Open-circuit gain]
# 
# An approximate equation for the output voltage is
# 
# $$V_{out} = A_d (V_+ - V_-) + A_c(V_+ + V_-)$$
# 
# where $A_d$ is the differential gain and $A_c$ is the common-mode gain. Normally we seek very high values for $A_d$ and very low values for $A_c$. The common-mode rejection ratio is
# 
# $$CMRR = 20 \log_{10}\frac{A_d}{A_c}$$
# 
# Typical values of $CCMR$ are 100db or greater indicating $A_d > 10^5A_c$

# ## Feedback

# In[ ]:




