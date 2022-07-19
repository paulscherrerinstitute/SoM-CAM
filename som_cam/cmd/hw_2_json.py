#!/usr/bin/env python3

import json

import click

from .utils import get_logger, update_logger


@click.command()
@click.option(
    "-i",
    "--input_file_name",
    help="The input json configuration file with the hardware details that should be read.",
)
@click.option(
    "-o",
    "--output_file_name",
    help="The output json configuration file that will be generated containing the current hardware configuration.",
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
    """
    Reads an input json configuration file with the predefined configurations, reads the current configurations from the hardware and saves it into an output json file.
    
    Examples:
    
        >>> som_cam hw-2-json -i /<path>/<to>/input_file.json -v DEBUG

    """

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
