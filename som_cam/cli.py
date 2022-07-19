import json
import logging
import pkgutil

import click

from .cmd.hw_2_json import hw_2_json
from .cmd.json_2_hw import json_2_hw


@click.group()
@click.version_option()
def main():  # pragma: no cover
    """
    SoM-CAM: CLI tooling interface for setting and getting configurations from hardwared.

    """
    pass


main.add_command(json_2_hw)
main.add_command(hw_2_json)
