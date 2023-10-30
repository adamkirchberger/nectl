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

import pytest
from unittest.mock import patch, ANY

from nectl.datatree.hosts import Host
from nectl.configs.drivers import run_driver_method_on_hosts
from nectl.exceptions import (
    DriverCommitDisconnectError,
    DriverError,
    DriverNotFoundError,
)


def test_should_log_warning_when_running_driver_method_on_invalid_host(
    mock_settings,
    caplog,
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN host with no os_name and mgmt_ip
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip=None,
        os_name=None,
        _facts={},
        _settings=None,
    )

    # GIVEN method name which should be irrelevant
    method_name = "foo"

    # WHEN running method
    total_errors, _ = run_driver_method_on_hosts(
        settings=mock_settings,
        hosts=[host],
        method_name=method_name,
        description=f"test {method_name} desc",
    )

    # THEN expect no errors as its just a warning
    assert total_errors == 0

    # THEN expect to have log with detailed error
    assert "skipping due to missing 'os_name' or 'mgmt_ip'" in caplog.text


@pytest.mark.parametrize(
    "method_name", ("get_config", "compare_config", "apply_config")
)
@patch("nectl.configs.drivers.get_driver")
def test_should_call_method_when_running_driver_method_on_hosts(
    mock_get_driver, mock_settings, method_name
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN method name
    method_name = method_name

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

    # GIVEN driver method returns mock diff
    getattr(
        mock_get_driver.return_value.return_value.__enter__.return_value, method_name
    ).return_value = "foodiff"

    # WHEN running method
    total_errors, outputs = run_driver_method_on_hosts(
        settings=mock_settings,
        hosts=[host],
        method_name=method_name,
        description=f"test {method_name} desc",
    )

    # THEN expect get driver to be called with settings and os_name
    mock_get_driver.assert_called_with(settings=mock_settings, os_name="fakeos")

    # THEN expect driver connection to be opened
    mock_get_driver.return_value.return_value.__enter__.assert_called()

    # THEN expect method to be called
    getattr(
        mock_get_driver.return_value.return_value.__enter__.return_value, method_name
    ).assert_called()

    # THEN expect output
    assert outputs == {"core0.london.acme": "foodiff"}

    # THEN expect no errors
    assert total_errors == 0


@pytest.mark.parametrize("method_name", ("apply_config",))
@patch("nectl.configs.drivers.get_driver")
def test_should_return_errors_when_running_driver_method_on_hosts_with_error_encountered(
    mock_get_driver, mock_settings, method_name
):
    # GIVEN mock settings
    mock_settings = mock_settings

    # GIVEN method name
    method_name = method_name

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

    # GIVEN driver method returns mock diff
    getattr(
        mock_get_driver.return_value.return_value.__enter__.return_value, method_name
    ).return_value = "foodiff"

    # GIVEN driver method raises DriverError
    mock_get_driver.return_value.return_value.__enter__.side_effect = DriverError

    # WHEN running method
    total_errors, outputs = run_driver_method_on_hosts(
        settings=mock_settings,
        hosts=[host],
        method_name=method_name,
        description=f"test {method_name} desc",
    )

    # THEN expect get driver to be called with settings and os_name
    mock_get_driver.assert_called_with(settings=mock_settings, os_name="fakeos")

    # THEN expect driver connection to be opened
    mock_get_driver.return_value.return_value.__enter__.assert_called()

    # THEN expect outputs to be empty
    assert outputs == {}

    # THEN expect 1 total errors
    assert total_errors == 1


@patch("nectl.configs.drivers.get_driver")
def test_should_return_diff_when_running_apply_method_and_host_disconnected_after_commit(
    mock_get_driver, mock_settings
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

    # GIVEN driver apply method raises DriverCommitDisconnectError
    mock_get_driver.return_value.return_value.__enter__.return_value.apply_config.side_effect = DriverCommitDisconnectError(
        diff="foodiff"
    )

    # WHEN running method
    total_errors, outputs = run_driver_method_on_hosts(
        settings=mock_settings,
        hosts=[host],
        method_name="apply_config",
        description=f"test apply_config desc",
    )

    # THEN expect get driver to be called with settings and os_name
    mock_get_driver.assert_called_with(settings=mock_settings, os_name="fakeos")

    # THEN expect driver connection to be opened
    mock_get_driver.return_value.return_value.__enter__.assert_called()

    # THEN expect outputs to include diff
    assert outputs == {"core0.london.acme": "foodiff"}

    # THEN 1 total errors
    assert total_errors == 1


@patch("nectl.configs.drivers.get_driver")
def test_should_return_errors_when_running_driver_methods_on_host_with_no_matching_driver(
    mock_get_driver, mock_settings
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

    # GIVEN get_driver method raises DriverNotFoundError
    mock_get_driver.side_effect = DriverNotFoundError

    # WHEN running method
    total_errors, outputs = run_driver_method_on_hosts(
        settings=mock_settings,
        hosts=[host],
        method_name="apply_config",
        description=f"test apply_config desc",
    )

    # THEN expect get driver to be called with settings and os_name
    mock_get_driver.assert_called_with(settings=mock_settings, os_name="fakeos")

    # THEN expect outputs to be empty
    assert outputs == {}

    # THEN expect 1 total errors
    assert total_errors == 1
