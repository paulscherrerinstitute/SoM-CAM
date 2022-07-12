#!/usr/bin/env python3

import click
import logging
from .utils import get_logger, set_logger_level

logger = get_logger()


@click.command()
@click.option('--file_name', help='JSON file name to be written')
@click.option('-v', '--verbose', type=click.Choice(['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], case_sensitive=False), help="Verbose level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
def Write(file_name, verbose):
    """Generate JSON file"""
    # # Generate JSON file
    # 
    # The following code writes a JSON hardware configuration to a file.
    # It utilizes the built-in json Python module to write a Python dictionary to a JSON file.
    update_logger(verbose)
    # with open(json_file, "r") as read_file:
    #     configurations = json.load(read_file)

    # for c in configurations.items():
    #     index = 0
    #     hw = c[1]
    #     for value in hw['settings']:
    #     # Call function to access hardware
    #         return_value = getattr(hw_access, 'set_' + hw['object'])(value, index)
    #         index += 1

