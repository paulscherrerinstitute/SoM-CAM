#!/usr/bin/env python3

import json

import click

from .hw_access import *
from .utils import get_logger, update_logger


@click.command()
@click.option("-i", "--input_file_name", help="JSON file name to be read")
@click.option(
    "-v",
    "--verbose",
    type=click.Choice(
        ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL",
)
def json_2_hw(input_file_name, verbose):
    """Read and execute JSON hardware configuration"""
    update_logger(verbose)
    log = get_logger()
    # The following code reads a JSON hardware configuration file. Every hardware object or circuit is configured by calling functions in the Python hw_access module.
    # E.g. the current_bias is set by calling the set_current_bias function.
    # Every hardware object requires a set_... function.
    try:
        log.info(f"Reading input configuration file {input_file_name}")
        with open(input_file_name, "r") as read_file:
            configurations = json.load(read_file)
    except IOError:
        error_msg = "Problem loading input configuration file..."
        raise Exception(error_msg)
    problem_flag = []
    for key, hw in configurations.items():
        index = 0
        log.debug(f"Key for this hw: { key }")
        for value in hw["settings"]:
            return_value = eval("set_" + hw["object"])(value, index)
            if return_value == False:
                log.critical(
                    f"Config { key} -> Problem setting configuration: { hw['object'] }"
                )
                problem_flag.append(hw["object"])
            log.debug(
                f"set_{ hw['object'] } ( value: { value }, channel: { index } ): return {return_value}"
            )
            index += 1
    if problem_flag:
        log.info(
            f"Configurations not fully set. Problems with { problem_flag } from file {input_file_name}"
        )
    else:
        log.info(
            f"Configurations successfully set. Json file: {input_file_name}."
        )
