# Basic Concepts

This page summarizes the data and model conventions used by `pyvrft`.

## Signals

Input and output signals are represented as NumPy matrices shaped `(N, n)`:

- `N` is the number of samples.
- `n` is the number of inputs or outputs.

For a SISO system, use one-column arrays shaped `(N, 1)` rather than one-dimensional vectors.

## Transfer functions

`pyvrft` uses SciPy discrete-time transfer functions, usually created with `dt=1`:

```python
from scipy import signal

G = signal.TransferFunction([1], [1, -0.9], dt=1)
```

When a numerator is one, use `[1]` rather than `[0, 1]` to avoid SciPy warnings.

## SISO systems

For SISO systems, some APIs accept a transfer function directly. Internally, `pyvrft` converts it to the same nested-list format used for MIMO systems.

```python
Td = signal.TransferFunction([0.2], [1, -0.8], dt=1)
L = signal.TransferFunction([0.25], [1, -0.75], dt=1)
```

## MIMO transfer matrices

MIMO transfer functions are represented as nested Python lists. The first index is the output and the second index is the input.

```python
G = [
    [G11, G12],
    [G21, G22],
]
```

Zero entries are written as the literal value `0`:

```python
Td = [
    [Td11, 0],
    [0, Td22],
]
```

## Controller structure

The controller structure `C` specifies the basis transfer functions used to estimate the controller parameters.

Each `C[i][j]` entry is a list of transfer functions for the subcontroller from output `j` to input `i`.

```python
Cpi = [
    [signal.TransferFunction([1, 0], [1, -1], dt=1)],
    [signal.TransferFunction([1], [1, -1], dt=1)],
]

C = [
    [Cpi, Cpi],
    [Cpi, Cpi],
]
```

Use an empty list `[]` when a subcontroller is absent.

The parameter vector returned by `vrft.design` is stacked by controller block, following the order documented in `vrft/control.py`.

## Instrumental variables

The third argument of `vrft.design` is `y_iv`, the output data used for instrumental variables.

Use the same output data for least-squares VRFT:

```python
p = vrft.design(u, y, y, Td, C, L)
```

Use a second output data set for instrumental-variable VRFT:

```python
p = vrft.design(u, ya, yb, Td, C, L)
```

## VRFT design objects

The main design call is:

```python
p = vrft.design(u, y, y_iv, Td, C, L)
```

where:

- `Td` is the desired closed-loop reference model.
- `C` is the controller structure.
- `L` is the VRFT pre-filter.
