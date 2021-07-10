
![Passing?](https://github.com/VOLTTRON/volttron-utils/actions/workflows/run-tests.yml/badge.svg)

VOLTTRON™ is an open source platform for distributed sensing and control. The platform provides services for collecting and storing data from buildings and devices and provides an environment for developing applications which interact with that data.

This repository contains utility classes and functions used in [volttron-client](https://github.com/VOLTTRON/volttron-client) and [volttron-server](https://github.com/VOLTTRON/volttron-server).

## Requirements

VOLTTRON is transitioning to using poetry as its base development and deployment environment.  Please
[install poetry](https://python-poetry.org/docs/#installation) before continuing.

## Installation

The volttron-utils package requires python >=3.6.2,<4.0 in order to run properly.  The volttron-utils package is available from pypi   To install into the current python environment use:

```bash
user@path$ pip install volttron-utils
```

## Development

To install development tools including pytest run

```bash
user@path$ poetry install
```

### Configuration

Its generally preferred to have the python environments created within the project directory.  Execute
this command to make that behavior the default.

```bash
user@path$ poetry config virtualenvs.in-project true
```

### Building Wheel

To build a wheel from this project execute the following:

```bash
user@path$ poetry build
```

The wheel and source distribution will be located in the ```./dist/``` directory.

### Bumping version number of project

To bump the version number of volttron-utils execute one of the following.

```bash
# patch, minor, major, prepatch, preminor, premajor, prerelease

# use patch
user@path$ poetry patch

# output
Bumping version from 0.2.0-alpha.0 to 0.2.0

# use prepatch
user@path$ poetry version prepatch

# output
Bumping version from 0.2.0 to 0.2.1-alpha.0
```

### Deployment to pypi

A github action has been created to allow for pushing the wheel to pypi.  The requirement for it is to create a tag using v*.*.* for the version of the file.  This can be done on a release basis or by pushing a local tag to github.  To push a local tag to github in the correct format use the following.

```bash
user@path$ git tag v0.0.1
user@path$ git push origin v0.0.1
```




