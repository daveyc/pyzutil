# pyzutil

z/OS utilities for Python

##  Building

```shell
python3 setup.py build

# Install in editable mode (i.e. setuptools "develop mode") from the local project path
pip3 install -e .
```

## Documentation

This project uses the [Sphinx](https://www.sphinx-doc.org/en/master/) Python Documentation Generator and requires the [Press](https://pypi.org/project/sphinx-press-theme/) theme.

To build the documentation run the following commands:
```shell
cd docs
make clean html
```