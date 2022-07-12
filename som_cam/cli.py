import click
import json
import logging
import pkgutil

from .cmd.read import Read
from .cmd.write import Write

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


main.add_command(Read)
main.add_command(Write)
