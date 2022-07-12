#!/usr/bin/env python3

import click
import logging

from .utils import get_logger, set_logger_level, update_logger

logger = get_logger()

@click.command()
@click.option('--file_name', help='JSON file name to be read')
@click.option('-v', '--verbose',type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False), help="Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
def Read(file_name, verbose):
    """Read and execute JSON hardware configuration"""
    
    # The following code reads a JSON hardware configuration file. Every hardware object or circuit is configured by calling functions in the Python hw_access module.
    # E.g. the current_bias is set by calling the set_current_bias function.
    # Every hardware object requires a set_... function.
    # with open(json_file, "r") as read_file:
    #     configurations = json.load(read_file)
    update_logger(verbose)
    # for c in configurations.items():
    #     index = 0
    #     hw = c[1]
    #     for value in hw['settings']:
    #     # Call function to access hardware
    #         return_value = getattr(hw_access, 'set_' + hw['object'])(value, index)
    #         index += 1
    