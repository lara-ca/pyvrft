# -*- coding: utf-8 -*-
"""
Created on Thu May 7 14:37:39 2026
@authors: Lara Colognese de Almeida
"""
"""
VRFT SISO example - Ill-conditioned Fisher information matrix
"""
#%% Header: importing python libraries

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import vrft

#%% Simulating the open-loop system to obtain data for the VRFT

# Declaration of the SISO transfer function of the process G(z)
G = signal.TransferFunction([1], [1, -0.9], dt=1)
# IMPORTANT: if the numerator of the transfer function is 1, define it as num=[1]
# num=[0,1] produces a warning!

# Number of samples
N = 100

# Step input signal (low spectral richness — poor persistent excitation)
u = np.ones((N, 1))
u[0] = 0
# IMPORTANT: signals are organized as matrices of shape (N, n),
# where N = number of samples and n = number of inputs/outputs

# Computing the system output
yu = vrft.filter(G, u)

# Adding white noise to the output
sigma2_e = 0.1
w = np.random.normal(0, np.sqrt(sigma2_e), N)
w.shape = (N, 1)

# Measured output
y = yu + w

#%% Graphics

lw = 1.5  # linewidth

# Input signal
plt.figure()
plt.plot(u, "b", drawstyle="steps", linewidth=lw, label="u(t)")
plt.grid(True)
plt.xlabel("Time (samples)")
plt.ylabel("u(t)")
plt.xlim(left=-2, right=N)
plt.show()

# Output signal
plt.figure()
plt.plot(y, "b", drawstyle="steps", linewidth=lw, label="y(t)")
plt.grid(True)
plt.xlabel("Time (samples)")
plt.ylabel("y(t)")
plt.xlim(left=-2, right=N)
plt.show()

#%% VRFT design parameters: reference model Td(z), filter L(z), controller structure

# Reference model Td(z)
Td = signal.TransferFunction([0.2], [1, -0.8], dt=1)

# Highly selective VRFT filter L(z): pole very close to z=1.
# high frequencies and making the regressors highly correlated.
L = signal.TransferFunction([0.001], [1, -0.999], dt=1)

# Controller structure with nearly redundant terms:
# making the columns of the regression matrix nearly linearly dependent.
C = [
    [signal.TransferFunction([1, 0], [1, -1],    dt=1)],  
    [signal.TransferFunction([1, 0], [1, -0.99], dt=1)],  
    [signal.TransferFunction([1, 0], [1, -0.98], dt=1)],  
]

#%% Controller design using the VRFT method

# VRFT with least squares — expects ill-conditioning warning
p, Z, min_eigenvalue = vrft.design_fisher(u, y, y, Td, C, L)
print("p =", p)
print("\nFisher information matrix Z:")
print(Z)
print("\nEigenvalues of Z:", np.linalg.eigvals(Z))
print("Condition number of Z:", np.linalg.cond(Z))
print("Min eigenvalue of Z:", min_eigenvalue)
# %%