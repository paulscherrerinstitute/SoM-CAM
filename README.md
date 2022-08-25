
# SoM-CAM


[![Conda](https://img.shields.io/conda/pn/paulscherrerinstitute/som_cam?color=success)](https://anaconda.org/paulscherrerinstitute/som_cam) [![GitHub](https://img.shields.io/github/license/paulscherrerinstitute/som-cam)](https://github.com/paulscherrerinstitute/som-cam/blob/master/LICENSE)[![CI](https://github.com/paulscherrerinstitute/SoM-CAM/actions/workflows/main.yml/badge.svg)](https://github.com/paulscherrerinstitute/SoM-CAM/actions/workflows/main.yml) [![GitHub Release Date](https://img.shields.io/github/release-date/paulscherrerinstitute/som-cam)](https://github.com/paulscherrerinstitute/SoM-CAM/releases) [![Upload Python Package](https://github.com/paulscherrerinstitute/SoM-CAM/actions/workflows/publish-conda-package.yml/badge.svg)](https://github.com/paulscherrerinstitute/SoM-CAM/actions/workflows/publish-conda-package.yml)


SoM-CAM configuration tool.

## Description

SoM-CAM tool allows users to (either locally on a device or remotely via ssh) configure parameters and quickly test configuration setups in special devices.

## Usage

To see help message, use `som_cam --help`

```bash
usage: som.py [-h] [--log {DEBUG,INFO,WARNING,ERROR,CRITICAL}] [--doc] [--path [PATH]] hostname function [args ...]

 SoM-CAM comissioning tool

positional arguments:
  hostname              HW hostname/device (local hostname is used by default)
  function              Name of the function to be executed
  args                  Arguments for the function.

options:
  -h, --help            show this help message and exit
  --log {DEBUG,INFO,WARNING,ERROR,CRITICAL}, -l {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level.
  --doc, -d
  --path [PATH], -p [PATH]
                        Folder that contains the hw_func file.
```

Example:

``` bash
som.py XCZU6EG-AD82 set_voltage 15 "'/tmp/voltage.txt'" --log DEBUG
```

## Special functions: get_all and set_all 

Auxiliary functions are provided to execute all possible functions available on the specified device (gets & sets).

### get_all

The get_all functionality will execute all the available 'get' functions from a specific device and store it into an output json file.

Example:
```bash
som.py XCZU6EG-AD82 get_all <output_file.json> --log DEBUG
```

### set_all

The set_all functionality will read a json file containing a device's configuration and will use all the 'set' functions to save the values from the input json file into the device's configuration.

Example:
```bash
som.py XCZU6EG-AD82 set_all <input_json> --log DEBUG
```

## Makefile 

A makefile is provided to facilitate some tasks, to see details use ```make help```:

```bash
Usage: make <target>

Targets:
help:             ## Show the help.
show:             ## Show the current environment.
fmt:              ## Format code using black & isort.
lint:                   ## Run pep8, black, mypy linters.
test: lint        ## Run tests and generate coverage report.
clean:            ## Clean unused files.
release:          ## Create a new tag for release.
docs:             ## Build the documentation.
init:             ## Initialize the project based on an application template.
```

## Contributors

- Ernst Johansen - ernst.johansen@psi.ch
- Leonardo Hax - leonardo.hax@psi.ch
- Tadej Humar - tadej.humar@psi.ch
- Thomas Jean Rossi - thomas.rossi1@psi.ch


