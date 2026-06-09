# API Reference

The package is installed from PyPI as `pyvrft`, but the Python import package is `vrft`.

```python
import vrft
```

The public API is re-exported from `vrft/__init__.py`.

## Main functions

### `vrft.design(u, y, y_iv, Td, C, L)`

Estimates controller parameters using the VRFT method.

Parameters:

- `u`: input data matrix shaped `(N, n)`.
- `y`: output data matrix shaped `(N, n)`.
- `y_iv`: output data matrix used for instrumental variables. Use `y_iv = y` for least-squares VRFT.
- `Td`: desired reference model.
- `C`: controller structure.
- `L`: VRFT pre-filter.

Returns:

- `p`: estimated controller parameter vector.

### `vrft.filter(G, u)`

Filters input data through a SISO or MIMO transfer function.

Parameters:

- `G`: SISO transfer function or MIMO transfer matrix represented as nested lists.
- `u`: input data matrix shaped `(N, m)`.

Returns:

- `y`: filtered output data matrix shaped `(N, n)`.

### `vrft.datafromcsv(file_name, delim, row_offset, n)`

Reads input/output data from a CSV file.

The CSV columns must be ordered as:

```text
y1, y2, ..., yn, u1, u2, ..., un
```

Parameters:

- `file_name`: CSV file path.
- `delim`: column delimiter, for example `","`.
- `row_offset`: number of header rows to skip.
- `n`: number of inputs and outputs.

Returns:

- `y`: output data matrix.
- `u`: input data matrix.

## Advanced utilities

### `vrft.mtf2ss(G)`

Converts a MIMO transfer-function matrix to a state-space model.

This is a simple conversion and does not produce a minimal realization.

Parameters:

- `G`: MIMO transfer-function matrix represented as nested lists.

Returns:

- `Ass`: state matrix.
- `Bss`: input matrix.
- `Css`: output matrix.
- `Dss`: feedforward matrix.

### `vrft.stbinv(A, B, C, D, y, t)`

Computes the stable inverse of an LTI system.

This is a lower-level utility used by the VRFT implementation.

Parameters:

- `A`, `B`, `C`, `D`: state-space matrices of the system to invert.
- `y`: output data matrix shaped `(p, N)`.
- `t`: time vector shaped `(1, N)`.

Returns:

- `uhat`: input signal calculated by the inversion algorithm.
- `tt`: time vector for `uhat`.
- `flag_vr`: inversion status flag.
