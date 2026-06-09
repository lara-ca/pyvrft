# Installation

## Install from PyPI

Install `pyvrft` with pip:

```bash
pip install pyvrft
```

The package name on PyPI is `pyvrft`, but the Python import package is `vrft`.

```python
import vrft
```

## Dependencies

`pyvrft` depends on:

- NumPy
- SciPy
- Matplotlib

These dependencies are installed automatically when installing the package with pip.

## Development installation

To install from a local checkout:

```bash
git clone https://github.com/datadrivencontrol/pyvrft
cd pyvrft
pip install .
```

## Verify the installation

Check that the package can be imported:

```bash
python -c "import vrft; print(vrft.__name__)"
```

If you are working from the repository, run the test suite from the repository root:

```bash
pytest
```
