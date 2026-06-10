# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:19:22 2026
@author: Lara Colognese de Almeida
"""
"""
Testing VRFT design with minimum-phase system and Td initialization method
"""

#%% Header: importing python libraries

import numpy as np  # important package for scientific computing
from scipy import signal  # signal processing library
import matplotlib.pyplot as plt  # library to plot graphics
import vrft  # vrft package

#%% Simulating the open loop system to obtain the data for VRFT

# declaration of the SISO transfer function of the process G(z)
# with zeros in -0.2 and 0.4, and poles in 0.8, 0.3, and 0
G = signal.TransferFunction([1, -0.2, -0.08], [1, -1.1, 0.24, 0], dt=1)

# number of samples
N = 200

# step reference signal
u = np.ones((N, 1))
u[N//2:N] = 0

# calculating the output of the system in open loop 
y = vrft.filter(G, u)

#%% Control - VRFT parameters: reference model Td(z) and controller structure

# declaration of the transfer function of the reference model Td(z)
Td = signal.TransferFunction([0.46009, 0, 0], [ 1, -0.361, -0.127784, -0.05112185], dt=1)

# defining PID controller structures for design
C_pid = [
    [signal.TransferFunction([1, 0, 0], [1, -1, 0], dt=1)],
    [signal.TransferFunction([1, 0],    [1, -1, 0], dt=1)],
    [signal.TransferFunction([1],       [1, -1, 0], dt=1)],
]

# VRFT with Td initialization for non-minimum-phase systems
eta, p =  vrft.design_nmp_Td_init(u, y, Td, C_pid, max_iter=30, tol=1e-5)

if np.any(np.abs(np.roots(eta.flatten())) > 1):
    print("\033[31mWarning: The identified Td has non-minimum-phase zeros.\033[0m")
else:
    print("\033[32mNo non-minimum-phase zeros identified.\033[0m")

print("Identified zeros:", np.roots(eta.flatten()))

# %%