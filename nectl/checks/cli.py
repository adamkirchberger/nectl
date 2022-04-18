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

import click

from ..logging import logging_opts


@click.group(help="Validation commands.")
@logging_opts
def checks():
    """
    Checks CLI group.
    """


@checks.command(name="list")
@click.pass_context
@logging_opts
def list_cmd(ctx):
    """
    Use this command to list all configured checks.
    """
    print("Not implemented.")


@checks.command(name="run")
@click.pass_context
@logging_opts
def run_cmd(ctx):
    """
    Use this command to run checks.
    """
    print("Not implemented.")
