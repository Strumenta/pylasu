import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "pylasu", '__version__.py')) as f:
    exec(f.read(), about)

setup(
    packages=find_packages(exclude=["tests"]),
    version=about['__version__'],
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
