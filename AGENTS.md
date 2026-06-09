# AGENTS.md

## Repo shape
- This is a small Python package named `pyvrft`; the import package is `vrft`.
- Public API is re-exported from `vrft/__init__.py`: `design`, `filter`, `stbinv`, `mtf2ss`, `datafromcsv`.
- Main implementation files are `vrft/control.py`, `vrft/invfunc.py`, and `vrft/csvfunc.py`.
- `build/lib/vrft/` is generated build output; do not edit it. Change source files under `vrft/`.

## Setup and verification
- Install locally with dependencies: `pip install .`
- Run the test suite from repo root: `pytest`
- Existing CI only installs with `pip install .` and runs `pytest`.
- There is no configured formatter, linter, type checker, or pyproject-based tool config in this repo.

## Tests
- Tests live in `tests/test_vrft.py` and use `unittest` assertions but are run by `pytest`.
- Run a focused test with: `pytest tests/test_vrft.py::TestVrft::test_tf2ss`

## Package conventions
- Signals are organized as NumPy matrices shaped `(N, n)`, where `N` is samples and `n` is number of inputs/outputs.
- MIMO transfer functions are represented as nested Python lists; zero entries are literal `0`.
- SISO transfer functions may be passed directly in some APIs and are converted internally to nested list form.
- The code expects SciPy discrete transfer functions, usually created with `signal.TransferFunction(..., dt=1)`.
- Examples warn that numerators like `[1]` should be used instead of `[0, 1]` to avoid SciPy warnings.

## Documentation direction
- Documentation site uses root `mkdocs.yml`, Markdown pages under `docs/`, Material for MkDocs, and `docs/CNAME`.
- The custom domain for this project is `pyvrft.net`; `docs/CNAME` contains this value for GitHub Pages.
- `/site/` is generated MkDocs build output and is ignored; do not edit or version it.
- Planned canonical repository is `https://github.com/datadrivencontrol/pyvrft`.
- DOI should be created through Zenodo connected to the GitHub repository, then recorded in package metadata, README, and documentation; create/update `CITATION.cff` only after the real Zenodo DOI exists.

## Examples
- Example scripts are under `example/`.
- `example/mimo_csv.py` reads `data.csv` using a relative path, so it should be run from the `example/` directory unless the path is adjusted.
