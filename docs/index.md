# Welcome to SoM-CAM documentation

SoM-CAM configuration tool


To see help message, use `som_cam --help`

```bash
Usage: python -m som_cam [OPTIONS] COMMAND [ARGS]...

  SoM-CAM: CLI tooling interface for setting and getting configurations from
  hardwared.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  hw-2-json  Reads an input json configuration file with the predefined...
  json-2-hw  Reads an input json hardware configuration file and...
```


## Commands help

* `hw-2-json`:

```bash
Usage: python -m som_cam hw-2-json [OPTIONS]

  Reads an input json configuration file with the predefined configurations,
  reads the current configurations from the hardware and saves it into an
  output json file.

  Examples:

      >>> som_cam hw-2-json -i /<path>/<to>/input_file.json -v DEBUG

Options:
  -i, --input_file_name TEXT      The input json configuration file with the
                                  hardware details that should be read.
  -o, --output_file_name TEXT     The output json configuration file that will
                                  be generated containing the current hardware
                                  configuration.
  -v, --verbose [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Verbose level: DEBUG, INFO, WARNING, ERROR,
                                  CRITICAL
  --help                          Show this message and exit.
```


* `json-2-hw`:

```bash
Usage: python -m som_cam json-2-hw [OPTIONS]

  Reads an input json hardware configuration file and configures the hardware
  by setting the values to it.

  Examples:     >>> som_cam hw-2-json -i /<path>/<to>/input_file.json -o
  /<path/<to>/output_file_to_be_generated.json -v DEBUG

Options:
  -i, --input_file_name TEXT      JSON file name to be read
  -v, --verbose [DEBUG|INFO|WARNING|ERROR|CRITICAL]
                                  Verbose level: DEBUG, INFO, WARNING, ERROR,
                                  CRITICAL
  --help                          Show this message and exit.
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

Ernst Johansen - ernst.johansen@psi.ch
Leonardo Hax - leonardo.hax@psi.ch
Tadej Humar - tadej.humar@psi.ch
Thomas Jean Rossi - thomas.rossi1@psi.ch


