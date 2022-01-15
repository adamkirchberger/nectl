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
            "mgmt_ip": None,
        }
    }

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output to match facts
    assert json.loads(result.output) == expected_facts
