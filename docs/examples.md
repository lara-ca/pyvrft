# Examples

Example scripts are available in the repository's `example/` directory.

The examples use Matplotlib and open figures when executed.

## Available examples

### `siso.py`

Designs a SISO PI controller using VRFT with least squares.

### `mimo.py`

Designs a MIMO PI controller using VRFT with instrumental variables. The example simulates two output data sets and passes them to `vrft.design` as `ya` and `yb`.

### `mimo_csv.py`

Designs a MIMO PI controller using data loaded from `data.csv` with `vrft.datafromcsv`.

This script reads the file with the relative path `"data.csv"`, so run it from inside the `example/` directory unless the path is changed.

### `siso_fisher.py`

Designs a SISO controller using VRFT with the Fisher information matrix method. Uses a step input and near-redundant controller terms to illustrate ill-conditioning of the Fisher matrix Z.

## Running the examples

Install the package first:

```bash
pip install .
```

Then run the examples from the `example/` directory:

```bash
cd example
python siso.py
python mimo.py
python mimo_csv.py
python siso_fisher.py
```

Running from `example/` is required for `mimo_csv.py` because of the relative `data.csv` path.
