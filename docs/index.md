# pyvrft - Virtual Reference Feedback Tuning

`pyvrft` is a Python toolbox for designing feedback controllers from input/output data using Virtual Reference Feedback Tuning (VRFT).

The package supports SISO and MIMO controller design with standard least-squares estimation and instrumental variables.

## Install

```bash
pip install pyvrft
```

## Quick Start

```python
import vrft

p = vrft.design(u, y, y, Td, C, L)
```

where `u` and `y` are input/output data, `Td` is the reference model, `C` is the controller structure, and `L` is the VRFT pre-filter.

Signals are represented as NumPy matrices shaped `(N, n)`, where `N` is the number of samples and `n` is the number of inputs or outputs.

## Features

- SISO and MIMO VRFT controller design
- Least-squares implementation
- Instrumental-variable implementation through a second output data set
- Filtering utilities for discrete-time transfer functions
- Stable inversion utilities for reference-model inversion
- CSV helper for loading input/output data

## Documentation

- [Installation](installation.md): install from PyPI or from a development checkout.
- [Quick Start](quickstart.md): design a first SISO controller with VRFT.
- [Basic Concepts](basic-concepts.md): signal shapes, transfer-function conventions, MIMO lists, and controller structures.
- [Examples](examples.md): runnable SISO, MIMO, and CSV examples from the repository.
- [API Reference](api.md): public functions re-exported by `vrft`.
- [Citation](citation.md): citation information and planned DOI workflow.

## Citation

A DOI will be added after the GitHub repository is connected to Zenodo and an archived release is created. See [Citation](citation.md).

## Links

- [GitHub](https://github.com/datadrivencontrol/pyvrft)
- [PyPI](https://pypi.org/project/pyvrft/)
