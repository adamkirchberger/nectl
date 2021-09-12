# Copyright (C) 2021 Adam Kirchberger
#
# This file is part of Nectl.
#
# Nectl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Nectl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nectl.  If not, see <http://www.gnu.org/licenses/>.

import sys
import click

from .logging import logging_opts
from .exceptions import ConfigFileError
from .config import APP_VERSION, APP_DESCRIPTION, get_config
from .data.cli import data
from .configs.cli import configs
from .templates.cli import templates
from .tests.cli import tests


def main():
    """
    Main entrypoint
    """
    return cli_root()  # pylint: disable=E1120


@click.group(help=APP_DESCRIPTION)
@click.version_option(APP_VERSION)
@click.pass_context
@logging_opts
def cli_root(ctx):
    """
    Root CLI group
    """
    # Load config file
    try:
        config = get_config()
    except ConfigFileError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Set context for child commands
    ctx.obj = {"config": config}


# Add child groups
cli_root.add_command(data)
cli_root.add_command(configs)
cli_root.add_command(templates)
cli_root.add_command(tests)
