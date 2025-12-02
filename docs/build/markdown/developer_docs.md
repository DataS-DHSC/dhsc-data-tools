# Developer documentation

## Developer setup

1. Clone this repository.
2. Install the package in editable mode including development and documentation dependencies from `pyproject.toml`.

```default
pip install -e ".[dev,docs]"
```

> When you make changes to the source code, run this again to update your local install with your changes.

## Updating the Sphinx documentation

1. Adjust the docstrings.
2. Edit static content, if needed, only in `docs/source`. (Likely `docs/source/_static`.)
3. Then run this to update the docs.

```default
sphinx-apidoc -o docs/source src/dhsc_data_tools && sphinx-build -M markdown docs/source/ docs/build/
```

## Building the package

With the relevant dependencies installed, you may build distributables:

```default
build .
```
