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


@click.group(help="device configuration commands")
@logging_opts
def configs():
    """
    Configs CLI group.
    """


@configs.command()
@click.pass_context
@logging_opts
def replace(ctx):
    """
    Use this command to replace config on remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def apply(ctx):
    """
    Use this command to apply config on a remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def diff(ctx):
    """
    Use this command to compare the intended vs actual config on remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def backup(ctx):
    """
    Use this command to make a local config backup from remote devices.
    """
    raise NotImplementedError
