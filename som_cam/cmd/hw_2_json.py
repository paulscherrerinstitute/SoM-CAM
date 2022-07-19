#!/usr/bin/env python3

import json

import click

from .utils import get_logger, update_logger


@click.command()
@click.option(
    "-i", "--input_file_name", help="JSON file containing the configurations"
)
@click.option(
    "-o",
    "--output_file_name",
    help="Output JSON file name that hw configuration will be saved.",
)
@click.option(
    "-v",
    "--verbose",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
)
def hw_2_json(input_file_name, output_file_name, verbose):
    """Generate JSON file"""
    # The following code writes a JSON hardware configuration to a file.
    # It utilizes the built-in json Python module to write a Python dictionary to a JSON file.
    update_logger(verbose)
    log = get_logger()
    # loads json configuration file
    try:
        log.info(f"Reading input configuration file {input_file_name}")
        with open(input_file_name, "r") as read_file:
            configurations = json.load(read_file)
    except IOError:
        error_msg = "Problem loading input configuration file..."
        raise Exception(error_msg)

    # gets the values from the hw
    config_dict = {}
    for key, value in configurations.items():
        log.debug(key)
        log.debug(value)
        log.debug(value["settings"])

        # log.debug(c)
        # index = 0
        # hw = c[1]
        # log.debug(hw["settings"])
        # for value in hw['settings']:
    #     # Call function to access hardware
    #         return_value = getattr(hw_access, 'get_' + hw['object'])(index)
    #         index += 1

    # Saves the output configuration file
    try:
        log.info(f"Creating output json file {output_file_name}")
        with open(output_file_name, "w") as outfile:
            json.dump(config_dict, outfile)
    except IOError:
        error_msg = "Problem saving output json configuration file..."
        raise Exception(error_msg)

    # with open(json_file, "r") as read_file:
    #     configurations = json.load(read_file)

