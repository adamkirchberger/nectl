import os
import click
from unittest.mock import patch

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

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect version unknown in output
    assert result.output.strip() == "cli-root, version unknown"


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
