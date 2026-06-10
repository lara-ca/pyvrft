#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 21 15:27:38 2026
@authors: Lara Colognese de Almeida
"""
#%% Header: import libraries

from scipy import signal  # signal processing library
import numpy as np  # important package for scientific computing
import vrft  # vrft package
from vrft.control import colfilter

#%% Function to check the conditioning of the Fisher information matrix Z


def check_Z(Z, threshold=1e-4):
    # Description to help the user
    """Function that checks the conditioning of the Fisher information matrix Z.
    
    Inputs: Z, threshold
    Outputs: Z, min_eig
    
    Inputs description:
        Z: Fisher information matrix. Its dimension must be (p_tot, p_tot), where p_tot is the total 
           number of controller parameters. It must be in the format of np.ndarray;
        threshold: Minimum acceptable ratio (relative eigenvalue ratio = min_eigenvalue / max_eigenvalue).
    
    Outputs description:
        Z: The original Fisher information matrix (returned unchanged). 
        min_eig: Absolute value of the smallest eigenvalue of Z. It is a float value."""

    # Calculate all eigenvalues of the Fisher information matrix
    eigenvalues = np.linalg.eigvals(Z)

    # Find the smallest and largest eigenvalues (in absolute value)
    min_eig = np.min(np.abs(eigenvalues))
    max_eig = np.max(np.abs(eigenvalues))

    # Compute the ratio of smallest to largest eigenvalue (inverse of condition number)
    # A higher ratio indicates better conditioning
    ratio = min_eig / max_eig

    # Check if the matrix is ill-conditioned and issue warning if necessary
    if ratio < threshold:
        print(
            f"\033[91mWarning! The min/max eigenvalue ratio of Z is {ratio:.2e}, "
            f"below the threshold {threshold:.2e} (condition number > {1/threshold:.0e}). "
            "The matrix may be ill-conditioned.\033[0m"
        )

    return Z, min_eig


#%% Function that designs the controller with the VRFT method and returns the Fisher Information Matrix


def design_fisher(u, y, y_iv, Td, C, L, threshold=1e-4):
    # Description to help the user
    """Function that designs the controller using the VRFT method with Fisher Information Matrix analysis.
    
    Inputs: u, y, y_iv, Td, C, L, threshold
    Outputs: p, Z
    
    Inputs description:
        u: input data matrix. The dimension of u must be (N,n), where N is the data length and n is the number of inputs/outputs of the system;
        y: output data matrix. The dimension of y must be (N,n), where N is the data length and n is the number of inputs/outputs of the system;
        y_iv: output data matrix for the instrumental variable. The dimension of y must also be (N,n). If the user doesn't have any instrumental variable data, then y_iv must be the same data matrix as y;
        Td: Reference Model transfer matrix. It must be a python list of TransferFunctionDiscrete elements. The dimension of the list must be (n,n);
        C: Controller structure that will be used on the method. It also must be a python list of TransferFunctionDiscrete elements. The dimension of the list must be (n,n);
        L: VRFT method filter. It also must be a python list of TransferFunctionDiscrete elements. The dimension of the list must be (n,n).
        
    Outputs description:
        p: controller parameters obtained by the VRFT method.
        The parameter vector p is organized as p=[p11^T p12^T ... p1n^T p21^T p22^T ... p2n^T ... pnn^T]^T.
        Each pij represents the parameter vector of each subcontroller Cij(z,pij).
        Z: Fisher Information Matrix used in the parameter estimation. It provides information about the 
        parameter identifiability and estimation accuracy. """

    # Test the SISO scenario and convert to list structure if necessary
    if isinstance(Td, signal.dlti):
        Td = [[Td]]
    if isinstance(L, signal.dlti):
        L = [[L]]
    if isinstance(C[0][0], signal.dlti):
        C = [[C]]

    # Calculate system dimensions and number of samples
    N = len(u)
    n = len(Td)
    # Create time vector for the inversion algorithm
    t = np.linspace(0, N - 1, N)
    t.shape = (1, N)

    # Filter the input signal with L
    uf = vrft.filter(L, u)

    # Transform the reference model to state-space form
    Atd, Btd, Ctd, Dtd = vrft.mtf2ss(Td)
    # Calculate virtual reference by stable inversion of primary dataset
    rv, _, flagvr = vrft.stbinv(Atd, Btd, Ctd, Dtd, y.T, t)
    rv = rv.T
    # Calculate virtual reference for instrumental variable dataset
    rv_iv, _, _ = vrft.stbinv(Atd, Btd, Ctd, Dtd, y_iv.T, t)
    rv_iv = rv_iv.T

    # Test if the inversion algorithm was successful
    if flagvr == 0:
        # Adjust data length to match virtual reference length
        N = rv.shape[0]
        y = y[0:N, :]
        y_iv = y_iv[0:N, :]
        # Compute virtual errors for both datasets
        ebar = rv - y
        ebar_iv = rv_iv - y_iv
        # Trim the filtered input signal
        uf = uf[0:N, :]

        # Calculate total number of controller parameters
        nbpar = np.zeros((n, n))
        for i in range(0, n):
            for j in range(0, n):
                nbpar[i][j] = len(C[i][j])
        p_tot = int(np.sum(nbpar))

        # Build regression matrices by filtering virtual errors through controller structure
        phi_iN_list = []
        csi_iN_list = []
        for i in range(0, n):
            phi_iN = np.empty((N, 0))
            csi_iN = np.empty((N, 0))
            for j in range(0, n):
                if len(C[i][j]) > 0:
                    # Filter primary error through controller element
                    phi_ijN = vrft.filter(C[i][j], ebar[:, j : j + 1])
                    # Filter instrumental variable error through controller element
                    csi_ijN = vrft.filter(C[i][j], ebar_iv[:, j : j + 1])
                    phi_iN = np.concatenate(
                        (phi_iN, phi_ijN), axis=1
                    )
                    csi_iN = np.concatenate(
                        (csi_iN, csi_ijN), axis=1
                    )
            phi_iN_list.append(phi_iN)
            csi_iN_list.append(csi_iN)

        # Build full regression matrices with VRFT filter L applied
        Phi_vrf = np.empty((0, p_tot))
        Csi_vrf = np.empty((0, p_tot))
        for i in range(0, n):
            Phi_row = np.empty((N, 0))
            Csi_row = np.empty((N, 0))
            for j in range(0, n):
                # Apply VRFT filter to regression columns
                Phi_ij = colfilter(L[i][j], phi_iN_list[j])
                Csi_ij = colfilter(L[i][j], csi_iN_list[j])
                Phi_row = np.concatenate(
                    (Phi_row, Phi_ij), axis=1
                )
                Csi_row = np.concatenate(
                    (Csi_row, Csi_ij), axis=1
                )
            Phi_vrf = np.concatenate((Phi_vrf, Phi_row), axis=0)
            Csi_vrf = np.concatenate((Csi_vrf, Csi_row), axis=0)

        # Stack input signal vector for MIMO compatibility
        Uf = np.empty((0, 1))
        for i in range(0, n):
            Uf = np.concatenate((Uf, uf[:, i : i + 1]), axis=0)

        # Solve instrumental variable problem using Fisher Information Matrix
        Z = np.matmul(Csi_vrf.T, Phi_vrf)
        Y = np.matmul(Csi_vrf.T, Uf)
        p = np.linalg.solve(Z, Y)

        # Check conditioning of the Fisher Information Matrix
        Z, min_eigenvalue = check_Z(Z, threshold=threshold)

        # Return controller parameters and Fisher Information Matrix
        return p, Z, min_eigenvalue

    elif flagvr == 1:
        # Inversion algorithm failed
        print(
            "It was not possible to calculate the virtual reference. The inversion algorithm has failed."
        )
        p = np.empty((0, 0))
        Z = np.empty((0, 0))
        min_eigenvalue = 0
        return p, Z, min_eigenvalue

    elif flagvr == 2:
        # Reference model inverse is unstable
        print(
            "The inverse of the reference model Td(z) is unstable. It is not recommended to proceed with the VRFT method. The algorithm was aborted!"
        )
        p = np.empty((0, 0))
        Z = np.empty((0, 0))
        min_eigenvalue
        return p, Z, min_eigenvalue