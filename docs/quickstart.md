# Quick Start

This example designs a SISO PI controller using VRFT with least squares.

## Generate input/output data

```python
import numpy as np
from scipy import signal
import vrft

G = signal.TransferFunction([1], [1, -0.9], dt=1)

N = 100
u = np.ones((N, 1))
u[0] = 0

y = vrft.filter(G, u)
```

Signals in `pyvrft` are organized as NumPy matrices shaped `(N, n)`, where `N` is the number of samples and `n` is the number of inputs or outputs.

## Define the VRFT design objects

```python
Td = signal.TransferFunction([0.2], [1, -0.8], dt=1)
L = signal.TransferFunction([0.25], [1, -0.75], dt=1)

C = [
    [signal.TransferFunction([1, 0], [1, -1], dt=1)],
    [signal.TransferFunction([1], [1, -1], dt=1)],
]
```

Here:

- `Td` is the desired closed-loop reference model.
- `L` is the VRFT pre-filter.
- `C` defines a PI controller structure.

## Estimate the controller parameters

```python
p = vrft.design(u, y, y, Td, C, L)
print(p)
```

The third argument is `y_iv`, the output data used for instrumental variables. Passing `y_iv = y` uses the same data set and gives the standard least-squares VRFT estimate.

## SciPy transfer-function note

When a transfer-function numerator is one, define it as `[1]` rather than `[0, 1]` to avoid SciPy warnings.
