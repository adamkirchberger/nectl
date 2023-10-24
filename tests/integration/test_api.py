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
from unittest.mock import patch, ANY

from nectl import Nectl
from nectl.datatree.hosts import Host
from nectl.exceptions import (
    DriverCommitDisconnectError,
    DriverError,
    DriverNotFoundError,
)


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
