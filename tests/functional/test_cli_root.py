# Copyright (C) 2022 Adam Kirchberger
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
import pkg_resources

from nectl.cli import cli_root
from nectl.settings import APP_VERSION


def test_should_return_usage_when_running_cli_with_no_args(cli_runner):
    # GIVEN args
    args = []

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect usage commands
    assert "Commands:" in result.output


def test_should_return_version_when_running_cli_with_version_arg(cli_runner):
    # GIVEN args
    args = ["--version"]

    # GIVEN version
    version = APP_VERSION

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect version unknown in output
    assert result.output.strip() == f"cli-root, version {version}"


def test_should_return_error_when_running_cli_with_no_config_file(cli_runner):
    # GIVEN args
    args = ["mock-command"]

    # GIVEN mock command
    cli_root.add_command(click.Command("mock-command"))

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be unsuccessful
    assert result.exit_code == 1

    # THEN expect error message
    assert "Error: settings file not found" in result.output
