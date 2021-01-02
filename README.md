# Python New Project Package

This repository holds a minimal but complete `python3` package
with the following quality services already included:

 - `setuptools` flow for packaging;
 - `unittest` test suite sub-package suited for Test Driven Development;
 - `coverage` for test suite;
 - `pylint` syntax checks;
 - `mypy` for type hints checks and errors;
 - `black` and `isort` for code formatting;
 - `jupyter` notebooks rendering (with Sphinx integration);
 - `Sphinx` documentation builder;
 - `anybadge` for any session badges;  
 - `nox` for session coordination;
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
nox -s tests
```

### Test coverage

To run the test suite coverage, issue:

```bash
nox -s coverage
```

### Refresh notebooks

To refresh all notebooks, first declare a new kernel with all dependencies installed.
This will point towards the above created virtual environment:

```bash
nox -s notebooks
```

### Build documentation

This package uses Sphinx to build documentation (see `docs/requirements.txt`).
To generate the package documentation, issue:

```bash
nox -s docs
```

### Check syntax

To check python syntax, issue:

```bash
nox -s linter
```

It will return the pylint score of the package and list all possible improvements.

### Check types

To check type hints and common errors, issue:

```bash
nox -s typehints
```

### Generate badges

All badges are automatically generated for each `nox` session.
