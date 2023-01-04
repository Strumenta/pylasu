# Pylasu – Python Language Support #

[![Build Status](https://github.com/Strumenta/pylasu/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/Strumenta/pylasu/actions/workflows/pythonapp.yml)
[![PyPI](https://img.shields.io/pypi/v/pylasu.svg)](https://pypi.org/project/pylasu)

Pylasu is an AST Library in the [StarLasu](https://github.com/Strumenta/StarLasu) family, targeting the Python language.

## Testing

```shell
python -m unittest discover tests 
```

## Linting

```shell
flake8 . && flake8 tests
```

## Packaging and distributing

Update version in pyproject.toml, setup.cfg and setup.py _(TODO do we need all three?)_, then run:

```shell
rm dist/*
python -m build
python -m twine upload dist/*
```

If all goes well, tag the release:

```shell
git tag 
```
