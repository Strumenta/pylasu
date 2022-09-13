from setuptools import find_packages, setup
setup(
    name='pylasu',
    packages=find_packages(exclude=["tests"]),
    version='0.2.0',
    description='Pylasu',
    author='Strumenta S.R.L.',
    license='Apache License V2',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest==4.4.1'],
    test_suite='tests',
)
