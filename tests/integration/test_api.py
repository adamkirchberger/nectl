# Copyright (C) 2023 Adam Kirchberger
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

import pytest
import pathlib
from unittest.mock import patch, ANY

from nectl import Nectl
from nectl.datatree.hosts import Host
from nectl.exceptions import (
    DriverCommitDisconnectError,
    DriverError,
    DriverNotFoundError,
)


def test_should_return_hosts_when_running_nectl_get_hosts_method(mock_settings):
    # GIVEN mock settings
    mock_settings = mock_settings

    # WHEN running get hosts method
    hosts = Nectl(settings=mock_settings).get_hosts()

    # THEN expect each result to be a dict
    assert isinstance(hosts, dict)

    # THEN expect host instances in results
    for host in hosts.values():
        assert isinstance(host, Host)

    # THEN expect total hosts
    assert len(hosts) == 8


def test_should_return_hosts_when_running_nectl_get_hosts_method_with_filter(
    mock_settings,
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host has custom fact
    (
        pathlib.Path(mock_settings.kit_path)
        / "datatree/customers/acme/sites/london/hosts/core0/fact.py"
    ).write_text(f'custom_fact = "foobar"\n')

    # WHEN running get hosts method with filter
    hosts = Nectl(settings=mock_settings).get_hosts(
        customer="acme", site="london", hostname="core0"
    )

    # THEN expect each result to be a dict
    assert isinstance(hosts, dict)

    # THEN expect one host
    assert len(hosts) == 1
    host = list(hosts.values())[0]

    # THEN expect host instance
    assert isinstance(host, Host)

    # THEN expect custom fact to be set
    assert host.custom_fact == "foobar"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_create_file_when_running_nectl_get_configs_method(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns no errors and outputs
    mock_driver_method.return_value = (0, {"core0.london.acme": "fooconfig"})

    # WHEN running backup method
    backups_dir = Nectl(settings=mock_settings).get_configs(
        hosts=[host],
    )

    # THEN expect our host file in the backups dir
    with open(
        f"{backups_dir}/core0.london.acme.{mock_settings.configs_file_extension}",
        "r",
        encoding="utf-8",
    ) as fh:
        assert fh.read() == "fooconfig\n"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_raise_error_and_create_file_when_running_nectl_get_with_driver_errors(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns 1 errors and outputs
    mock_driver_method.return_value = (1, {"core0.london.acme": "fooconfig"})

    # WHEN running backup method
    with pytest.raises(DriverError) as error:
        backups_dir = Nectl(settings=mock_settings).get_configs(
            hosts=[host],
        )

        # THEN expect error message
        assert "1 errors encountered" in str(error.value)

        # THEN expect our host file in the backups dir
        with open(
            f"{backups_dir}/core0.london.acme.{mock_settings.configs_file_extension}",
            "r",
            encoding="utf-8",
        ) as fh:
            assert fh.read() == "fooconfig\n"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_create_file_when_running_nectl_diff_configs_method(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns no errors and outputs
    mock_driver_method.return_value = (0, {"core0.london.acme": "foodiff"})

    # WHEN running diff method
    diffs_dir = Nectl(settings=mock_settings).diff_configs(
        hosts=[host],
    )

    # THEN expect our host file in the diffs dir
    with open(
        f"{diffs_dir}/core0.london.acme.diff.{mock_settings.configs_file_extension}",
        "r",
        encoding="utf-8",
    ) as fh:
        assert fh.read() == "foodiff\n"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_raise_error_and_create_file_when_running_nectl_diff_with_driver_errors(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns 1 errors and outputs
    mock_driver_method.return_value = (1, {"core0.london.acme": "foodiff"})

    # WHEN running diff method
    with pytest.raises(DriverError) as error:
        diffs_dir = Nectl(settings=mock_settings).diff_configs(
            hosts=[host],
        )

        # THEN expect error message
        assert "1 errors encountered" in str(error.value)

        # THEN expect our host file in the diffs dir
        with open(
            f"{diffs_dir}/core0.london.acme.diff.{mock_settings.configs_file_extension}",
            "r",
            encoding="utf-8",
        ) as fh:
            assert fh.read() == "foodiff\n"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_create_file_when_running_nectl_apply_configs(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns no errors and outputs
    mock_driver_method.return_value = (0, {"core0.london.acme": "foodiff"})

    # WHEN running apply method
    diffs_dir = Nectl(settings=mock_settings).apply_configs(
        hosts=[host],
    )

    # THEN expect our host file in the diffs dir
    with open(
        f"{diffs_dir}/core0.london.acme.diff.{mock_settings.configs_file_extension}",
        "r",
        encoding="utf-8",
    ) as fh:
        assert fh.read() == "foodiff\n"


@patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_raise_error_and_create_file_when_running_nectl_apply_with_driver_errors(
    mock_driver_method, mock_settings
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # GIVEN driver method returns 1 errors and outputs
    mock_driver_method.return_value = (1, {"core0.london.acme": "foodiff"})

    # WHEN running apply method
    with pytest.raises(DriverError) as error:
        diffs_dir = Nectl(settings=mock_settings).apply_configs(
            hosts=[host],
        )

        # THEN expect error message
        assert "1 errors encountered" in str(error.value)

        # THEN expect our host file in the diffs dir
        with open(
            f"{diffs_dir}/core0.london.acme.diff.{mock_settings.configs_file_extension}",
            "r",
            encoding="utf-8",
        ) as fh:
            assert fh.read() == "foodiff\n"


def test_should_return_checks_when_running_nectl_list_checks(
    mock_settings, mock_checks_generator
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # WHEN listing checks
    checks = Nectl(settings=mock_settings).list_checks(hosts=[host])

    # THEN expect result to be list
    assert isinstance(checks, list)

    # THEN expect total checks
    assert len(checks) == 3

    # THEN expect checks
    assert checks == [
        "check_four.py::CheckLondon::check_site[core0.london.acme]",
        "check_one.py::check_os_version[core0.london.acme]",
        "check_three.py::CheckOsVersion::check_os_version[core0.london.acme]",
    ]


# @patch("nectl.nectl.run_driver_method_on_hosts")
def test_should_return_check_results_when_running_nectl_run_checks(
    mock_settings, mock_checks_generator
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="fakeos",
        _facts={},
        _settings=None,
    )

    # WHEN running checks
    result = Nectl(settings=mock_settings).run_checks(hosts=[host])

    # THEN expect result to be dict
    assert isinstance(result, dict)

    # THEN expect result
    assert result == {
        "passed": 1,
        "failed": 2,
        "report": f"{settings.kit_path}/{settings.checks_report_filename}",
    }
