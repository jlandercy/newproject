# Python New Project Package

This repository holds a minimal `python3` package with the following services
already included:

 - `setuptools` flow for packaging;
 - Test Suite sub-package for Test Driven Development;
 - Code Coverage for Test Suite;
 - PyLint syntax checking; 
 - Sphinx documentation builder (including notebooks rendering);
 - GitHub or GitLab CI/CD flows.

## How to?

### Start a new project

To start a new project from this package few steps are required:

 1. Fork this [repository](https://github.com/jlandercy/newproject) to your hub
    account and rename it;
 2. Clone the forked repository to your workspace;
 3. Rename the project by renaming the package directory;
 4. Start to implement your project as usual.

### Install package

Create a virtual environment if required and activate it:

```bash
python3 -m virtualenv venv
source venv/bin/activate
```

This package follows the usual `setuptools` flow, installation is as simple as:

```bash
python3 setup.py install
```

This will install dependencies as well (as defined in `requirements.txt`).

To build a wheel and install from it, then issue:

```bash
python3 setup.py sdist bdist_wheel
python3 -m pip install ./dist/*.whl
```

### Test package

To run the complete package test suite, issue:

```bash
python -m unittest discover -v newproject.tests
```

### Test coverage

To run the test suite coverage, issue:

```bash
python3 -m coverage run -m unittest discover -v newproject.tests
python3 -m coverage report
```

### Build documentation

This package uses Sphinx to build documentation (see `docs/requirements.txt`).
To generate the package documentation, issue:

```bash
make --directory=./docs/ html
```

### Refresh notebooks

To refresh all notebooks, first declare a new kernel with all dependencies installed.
This will point towards the above created virtual environment:

```bash
python3 -m ipykernel install --name=venv
```

Then refresh all notebooks using the above defined kernel:

```bash
python3 -m jupyter nbconvert --debug \
        --ExecutePreprocessor.timeout=600 \
        --ExecutePreprocessor.kernel_name=venv \
        --inplace --clear-output --to notebook \
        --execute ./docs/source/notebooks/*.ipynb
```

### Check syntax

To check python syntax, issue:

```bash
pylint newproject
```

It will return the pylint score of the package and list all possible improvements.

### Generate badges

To generate badges, issue the following commands:

```bash
anybadge --label=pylint --value=2.22 --file=docs/sources/badges/pylint.svg 2=red 4=orange 8=yellow 10=green
anybadge --label=coverage --value=65 --file=docs/sources/badges/coverage.svg
anybadge --label=pipeline --value=passing --file=docs/sources/badges/pipeline.svg passing=green failing=red
```