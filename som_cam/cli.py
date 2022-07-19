import json
import logging
import pkgutil

import click

from .cmd.hw_2_json import hw_2_json
from .cmd.json_2_hw import json_2_hw

"""
CLI interface for som_cam project.

"""


@click.group()
@click.version_option()
def main():  # pragma: no cover
    """
    More to come later
    """
    pass


main.add_command(json_2_hw)
main.add_command(hw_2_json)
