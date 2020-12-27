# Python New Project Package

This repository holds a minimalistic new `python3` package with the following service
already included:

 - `setuptools` flow for packaging;
 - Test Suite sub-package for Test Driven Development;
 - Sphinx documentation builder (including notebooks rendering);
 - PyLint syntax checking;
 - GitHub or GitLab CI/CD flows.

## How to...

### ...Start new project?

To start a new project from this package few steps are required:

 1. Fork the [repository](https://github.com/jlandercy/newproject) to your hub
    account and rename it at will;
 2. Clone the forked repository to your workspace:
    `git clone https://github.com/<user>/<repo>`;
 3. Rename the project by renaming the package directory:
    `mv newproject myproject`;
 4. Start to implement your project as usual.

### ...Install?

Create a virtual environment if required and activate it:

```bash
python3 -m virtualenv venv
source venv/bin/activate
```

This package follows the usual `setuptools` flow, installation is as simple as:

```bash
python3 setup.py install
```

This will install dependencies as well (as defined in `requirements.txt`)

To build a wheel and install from it, then issue:

```bash
python3 setup.py sdist bdist_wheel
python3 -m pip install ./dist/*.whl
```

### ...Build documentation?

This package use Sphinx to build documentation (see `docs/requirements.txt`).
To generate the package documentation, issue:

```bash
make --directory=./docs/ html
```

### ...Refresh notebooks?

To refresh all notebooks, first declare a new kernel with all dependencies installed.
This will point towards the above created virtual environment:

```bash
python3 -m ipykernel install --name=venv
```

Then refresh all notebooks using the kernel:

```bash
python3 -m jupyter nbconvert --debug \
        --ExecutePreprocessor.timeout=600 \
        --ExecutePreprocessor.kernel_name=venv \
        --inplace --clear-output --to notebook \
        --execute ./docs/source/notebooks/*.ipynb
```

### ...Check syntax?

To check python syntax, issue:

```bash
pylint newproject
```
