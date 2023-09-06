import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __version__.py module as a dictionary.
about = {}
with open(os.path.join(here, "pylasu", '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name='pylasu',
    packages=find_packages(exclude=["tests"]),
    version=about['version'],
    description='Pylasu is an AST Library in the StarLasu family, targeting the Python language.',
    author='Strumenta S.R.L.',
    license='Apache License V2',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
