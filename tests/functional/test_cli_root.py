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

import os
import click
from unittest.mock import patch
import pkg_resources

import nectl.config
from nectl.cli import cli_root


def test_should_return_usage_when_running_cli_with_no_args(cli_runner):
    # GIVEN args
    args = []

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect tool name in output
    assert "Network Control Tool" in result.output

    # THEN expect usage commands
    assert "Commands:" in result.output


def test_should_return_version_when_running_cli_with_version_arg(cli_runner):
    # GIVEN args
    args = ["--version"]

    # GIVEN version
    try:
        version = pkg_resources.get_distribution("nectl").version
    except pkg_resources.DistributionNotFound:
        version = "unknown"

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
    assert "Error: config file not found" in result.output


def test_should_return_hosts_when_running_cli_data_list_hosts_command(
    cli_runner, mock_config
):
    # GIVEN args
    args = ["data", "list-hosts"]

    # GIVEN expected hosts
    hosts = [
        "core0.newyork.acme",
        "core0.london.acme",
        "core0.newyork.hooli",
        "core0.london.hooli",
    ]

    # GIVEN get_config() is patched to return mock_config
    nectl.config.__config = mock_config

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect hosts to be listed
    for host in hosts:
        assert host in result.output, f"host '{host}' not found in hosts table"
