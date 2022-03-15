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

import pathlib
import pytest

from nectl.configs.drivers import get_driver
from nectl.configs.drivers.utils import load_drivers_from_kit
from nectl.exceptions import DriverLoadError


def test_should_return_blank_when_loading_kit_drivers_and_no_drivers_in_kit(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN drivers path is set to path that does not exist
    settings.drivers_dirname = "foodrivers"

    # WHEN loading drivers from kit
    drivers = load_drivers_from_kit(settings)

    # THEN expect blank
    assert drivers == {}


def test_should_raise_error_when_loading_kit_drivers_and_driver_invalid_syntax(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN drivers path
    drivers_path = pathlib.Path(settings.kit_path) / settings.drivers_dirname
    drivers_path.mkdir()

    # GIVEN custom driver fakeos
    (drivers_path / "fakeos.py").write_text("!!")

    # WHEN loading drivers from kit
    with pytest.raises(SyntaxError) as error:
        load_drivers_from_kit(settings)

    # THEN expect error
    assert "invalid syntax" in str(error.value)


def test_should_raise_error_when_loading_kit_drivers_and_driver_not_subclass(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN drivers path
    drivers_path = pathlib.Path(settings.kit_path) / settings.drivers_dirname
    drivers_path.mkdir()

    # GIVEN custom driver fakeos
    (drivers_path / "fakeos.py").write_text("class FakeOsDriver:\n" "    pass\n")

    # WHEN loading drivers from kit
    with pytest.raises(DriverLoadError) as error:
        load_drivers_from_kit(settings)

    # THEN expect error
    assert "driver 'fakeos' must be subclass of 'BaseDriver" in str(error.value)


def test_should_return_drivers_when_loading_kit_drivers(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN drivers path
    drivers_path = pathlib.Path(settings.kit_path) / settings.drivers_dirname
    drivers_path.mkdir()

    # GIVEN custom driver fakeos
    (drivers_path / "fakeos.py").write_text(
        "from nectl import BaseDriver\n"
        "class FakeOsDriver(BaseDriver):\n"
        "    foo = 'bar'\n"
    )

    # GIVEN custom driver spoofos
    (drivers_path / "spoofos.py").write_text(
        "from nectl import BaseDriver\n"
        "class SpoofOsDriver(BaseDriver):\n"
        "    foo = 'bar'\n"
    )

    # WHEN loading drivers from kit
    drivers = load_drivers_from_kit(settings)

    # THEN expect two drivers
    assert len(drivers) == 2

    # THEN expect drivers
    assert "fakeos" in drivers
    assert "spoofos" in drivers


def test_should_return_kit_driver_when_getting_driver(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN os_name
    os_name = "fakeos"

    # GIVEN drivers path
    drivers_path = pathlib.Path(settings.kit_path) / settings.drivers_dirname
    drivers_path.mkdir()

    # GIVEN custom driver fakeos
    (drivers_path / "fakeos.py").write_text(
        "from nectl import BaseDriver\n"
        "class FakeOsDriver(BaseDriver):\n"
        "    foo = 'bar'\n"
    )

    # WHEN getting driver
    driver = get_driver(settings=settings, os_name=os_name)

    # THEN expect driver
    assert driver is not None
