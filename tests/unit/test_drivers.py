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

from nectl.datatree.hosts import Host
from nectl.configs.drivers import get_driver, NapalmDriver
from nectl.exceptions import DriverError, DriverNotConnectedError, DriverNotFoundError


@pytest.mark.parametrize("driver_class", (NapalmDriver,))
def test_should_raise_error_when_instantiating_driver_on_host_with_no_mgmt_ip(
    driver_class,
):
    # GIVEN host with no mgmt_ip
    host = Host(
        hostname="core0", site="london", customer="acme", _facts={}, _settings=None
    )

    # GIVEN should raise error
    with pytest.raises(DriverError) as error:
        # WHEN instantiating host driver
        driver_class(host=host, username="testuser")

    # THEN expect error message
    assert str(error.value) == "host has no mgmt_ip"


@pytest.mark.parametrize("driverclass", (NapalmDriver,))
def test_should_raise_error_when_running_driver_methods_outside_context_manager(
    driverclass, mock_settings
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN host
    host = Host(hostname="core0", site="london", mgmt_ip="10.0.0.1", _settings=settings)

    # GIVEN driver instance
    driver = driverclass(host=host, username="foo")

    # GIVEN methods and args
    methods = {
        "get_config": {},
        "compare_config": {"config_filepath": None},
        "apply_config": {"config_filepath": None},
    }

    for method, args in methods.items():
        with pytest.raises(DriverNotConnectedError) as error:
            # WHEN calling get_config method without context
            getattr(driver, method)(**args)

        # THEN expect error message
        assert str(error.value) == f"'{method}' must be run within context manager"


@pytest.mark.parametrize(
    "os_name, expected_driver", (("junos", NapalmDriver), ("eos", NapalmDriver))
)
def test_should_return_driver_when_getting_driver_using_os_name(
    mock_settings,
    os_name,
    expected_driver,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN os_name
    os_name = os_name

    # WHEN calling get_driver using os_name
    driver = get_driver(settings, os_name)

    # THEN expect driver to match
    assert driver == expected_driver


def test_should_raise_error_when_getting_driver_that_does_not_exist(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN os_name
    os_name = "foobar"

    with pytest.raises(DriverNotFoundError) as error:
        # WHEN calling get_driver using os_name
        get_driver(mock_settings, os_name)

    # THEN expect error
    assert str(error.value) == "no driver found that matches os_name: foobar"


def test_should_return_driver_when_no_match_and_specified_default_driver_exists(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN default driver is set
    settings.default_driver = "napalm"

    # GIVEN os_name
    os_name = "foobar"

    # WHEN calling get_driver using os_name
    driver = get_driver(settings, os_name)

    # THEN expect driver to match
    assert driver == NapalmDriver


def test_should_raise_error_when_no_match_and_specified_default_driver_does_not_exist(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN default driver is set
    settings.default_driver = "magicdriver"

    # GIVEN os_name
    os_name = "foobar"

    with pytest.raises(DriverNotFoundError) as error:
        # WHEN calling get_driver using os_name
        get_driver(mock_settings, os_name)

    # THEN expect error
    assert str(error.value) == "no default driver found matching name: magicdriver"
