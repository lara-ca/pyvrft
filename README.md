# pyvrft

Virtual Reference Feedback Tuning Toolbox

## Description

This Python toolbox provides commands to design feedback controllers using Virtual Reference Feedback Tuning.
The toolbox implements SISO and MIMO controller design using standard least-squares estimation and instrumental variables.

## Documentation

Documentation is available at <https://pyvrft.net/>.

## Install

Use PIP to install:

```bash
pip install pyvrft
```

The package name on PyPI is `pyvrft`, but the Python import package is `vrft`.

## Use

Please check the *example* folder. Basic use:

```Python
p = vrft.design(u, y, y, Td, C, L)
```
where *u* and *y* are input/output data, *Td* is the reference model, *C* describes the controller structure and *L* is a pre-filter.

## Citation

A DOI will be added after the GitHub repository is connected to Zenodo and an archived release is created.
For current citation guidance, see <https://pyvrft.net/citation/>.

## Contributors

Diego Eckhard - diegoeck@ufrgs.br - @diegoeck

Emerson Christ Boeira - emerson.boeira@ufrgs.br - @emersonboeira
