import click
import json

import nectl.config
from nectl.cli import cli_root


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


def test_should_return_hosts_when_running_cli_data_get_facts_command(
    cli_runner, mock_config
):
    # GIVEN args
    args = ["data", "get-facts", "-h", "core0", "-s", "london", "-c", "acme"]

    # GIVEN expected output
    expected_facts = {
        "core0.london.acme": {
            "id": "core0.london.acme",
            "hostname": "core0",
            "site": "london",
            "customer": "acme",
            "role": None,
            "manufacturer": None,
            "model": None,
            "os_name": "fakeos",
            "os_version": "1.2.3",
            "serial_number": None,
            "asset_tag": None,
        }
    }

    # GIVEN get_config() is patched to return mock_config
    nectl.config.__config = mock_config

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output to match facts
    assert json.loads(result.output) == expected_facts
