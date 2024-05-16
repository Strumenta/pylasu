# Pylasu – Python Language Support #

[![Build Status](https://github.com/Strumenta/pylasu/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/Strumenta/pylasu/actions/workflows/pythonapp.yml)
[![PyPI](https://img.shields.io/pypi/v/pylasu.svg)](https://pypi.org/project/pylasu)
[![Documentation](https://readthedocs.org/projects/pylasu/badge/?version=latest&style=flat)](https://pylasu.readthedocs.io)

Pylasu is an AST Library in the [StarLasu](https://github.com/Strumenta/StarLasu) family, targeting the Python language. [Documentation](https://pylasu.readthedocs.io) is on Read the Docs.

## Testing

```shell
python -m unittest discover tests 
```

## Linting

```shell
flake8 . && flake8 tests
```

## Testing

```shell
pytest tests
```

## Packaging and Distribution

Update version in `setup.cfg` and `pylasu/__version__.py` _(TODO do we need both?)_,
commit and check that CI completes normally. 

Let's ensure that we have build and twine installed:

```shell
pip install build twine
```

Then, check the project can be released by linting and running the test suite:

```shell
flake8 . && flake8 tests
pytest tests
```

Finally, we can run:

```shell
rm dist/*
python -m build
python -m twine upload dist/*
```

**Note:** if we have [two-factor authentication (2FA)](https://pypi.org/help/#twofa) enabled on PyPI, 
we have to [use an API token](https://pypi.org/help/#apitoken).

If all goes well, tag the release:

```shell
git tag 
```

### Extracting Documentation

Here's how to extract the documentation into HTML using Sphinx, the most popular documentation generator for Python.

First, ensure you have Sphinx and the chosen theme installed:
```shell
pip install sphinx sphinx_rtd_theme
```

Then, extract the documentation from the source code:
```shell
sphinx-apidoc -o docs pylasu
```

Finally, change into the docs directory and launch the build process:
```shell
cd docs
make html
```

If everything goes as it should, in `docs/_build/html` you'll find the generated documentation.

We also host the documentation on ReadTheDocs. The project is [pylasu](https://readthedocs.org/projects/pylasu/). 
Documentation needs to be [built manually](https://readthedocs.org/projects/pylasu/) for each release for it to appear
online on https://pylasu.readthedocs.io.
