# -*- coding: utf-8 -*-
"""
Created on Mon May 11 09:19:22 2026
@author: Lara Colognese de Almeida
"""
"""
Testing VRFT design with non-minimum-phase system with closed loop initialization method
"""

#%% Header: importing python libraries

import numpy as np  # important package for scientific computing
from scipy import signal  # signal processing library
import matplotlib.pyplot as plt  # library to plot graphics
import vrft  # vrft package

#%% Simulating the closed-loop system to obtain the data for VRFT

# declaration of the SISO transfer function of the process G(z)
# with zeros in 1.2 (non minimum phase) and 0.4, and poles in 0.8, 0.3, and 0
G = signal.TransferFunction([1, -1.6, 0.48], [1, -1.1, 0.24, 0], dt=1)

# number of samples
N = 200

# step reference signal
u = np.ones((N, 1))
u[N//2:N] = 0

# calculating open-loop output
y = vrft.filter(G, u)

#%% Graphics

lw=1.5 # linewidth

# plot reference and output for open-loop simulation
plt.figure()
plt.plot(u, drawstyle="steps", linewidth=lw, label="u(t)")
plt.plot(y, drawstyle="steps", linewidth=lw, label="y(t)")
plt.grid(True)
plt.title("Open-loop response")
plt.xlabel("time (samples)")
plt.xlim(left=-2, right=N)
plt.legend()
plt.show()

#%% Control - VRFT parameters: reference model Td(z) and controller structure

# declaration of the transfer function of the reference model Td(z)
Td = signal.TransferFunction([0.07061, 0, 0], [ 1, -1.591,  0.94481, -0.2832 ], dt=1)

# defining PID controller structures for design
C_pid = [
    [signal.TransferFunction([1, 0, 0], [1, -1, 0], dt=1)],
    [signal.TransferFunction([1, 0],    [1, -1, 0], dt=1)],
    [signal.TransferFunction([1],       [1, -1, 0], dt=1)],
]

#%% VRFT with Td initialization for non-minimum-phase systems - open loop

eta, p =  vrft.design_nmp_Td_init(u, y, Td, C_pid, max_iter=80, tol=1e-5, filter=True)

if np.any(np.abs(np.roots(eta.flatten())) > 1):
    print("\033[31mWarning: The identified Td has non-minimum-phase zeros.\033[0m")
else:
    print("\033[32mNo non-minimum-phase zeros identified.\033[0m")

print("Identified zeros:", np.roots(eta.flatten()))

#%% Mismatch case - changing the reference model - closed loop 

# declaration of the transfer function of the reference model Td(z)
Td_mismatch = signal.TransferFunction([0.064, 0, 0], [ 1, -1.8,  1.08 , -0.216], dt=1)

eta, p =  vrft.design_nmp_Td_init(u, y, Td_mismatch, C_pid, max_iter=300, tol=1e-5, filter=True)

if np.any(np.abs(np.roots(eta.flatten())) > 1):
    print("\033[31mWarning: The identified Td has non-minimum-phase zeros.\033[0m")
else:
    print("\033[32mNo non-minimum-phase zeros identified.\033[0m")

print("Identified zeros:", np.roots(eta.flatten()))
# %%