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
from .exceptions import SettingsFileError
from .settings import APP_VERSION, APP_DESCRIPTION, get_settings
from .datatree.cli import datatree
from .configs.cli import configs
from .checks.cli import checks


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
    # Load settings file
    try:
        settings = get_settings()
    except SettingsFileError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Set context for child commands
    ctx.obj = {"settings": settings}


# Add child groups
cli_root.add_command(datatree)
cli_root.add_command(configs)
cli_root.add_command(checks)
