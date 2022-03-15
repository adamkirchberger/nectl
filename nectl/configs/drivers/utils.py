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
import sys
import importlib
from typing import Dict

from nectl.exceptions import DriverLoadError

from ...logging import get_logger
from ...settings import Settings
from .basedriver import BaseDriver

logger = get_logger()


def load_drivers_from_kit(settings: Settings) -> Dict[str, BaseDriver]:
    """
    Returns a dict of os_name and driver objects found in kit.

    Args:
        settings (Settings): config settings.

    Returns:
        Dict[str,BaseDriver]: os_name as key and driver object as value.
    """
    # Build drivers full path
    drivers_path = os.path.join(settings.kit_path, settings.drivers_dirname)

    # Check if any kit drivers exist
    if not os.path.exists(drivers_path):
        logger.debug("no drivers directory found in kit")
        return {}

    logger.info("loading drivers from kit")

    # ensure kit path is in pythonpath
    if sys.path[0] != settings.kit_path:
        logger.debug(f"appending kit to PYTHONPATH: {settings.kit_path}")
        sys.path.insert(0, settings.kit_path)

    drivers = {}

    for driver_filename in os.listdir(drivers_path):
        # Remove extension from driver filename
        driver_filename = driver_filename.replace(".py", "")

        # Import driver module
        driver = importlib.import_module(
            settings.drivers_dirname + "." + driver_filename
        )

        # Fetch driver class named like file
        for var, obj in driver.__dict__.items():
            # Look for class name '<filename>Driver'
            if var.lower() == f"{driver_filename.lower()}driver":
                # Ensure that driver is child of base driver
                if not issubclass(obj, BaseDriver):
                    raise DriverLoadError(
                        f"driver '{driver_filename}' must be subclass of 'BaseDriver'"
                    )

                # Add driver
                drivers[driver_filename] = obj
                break

    if drivers:
        logger.debug(f"found kit drivers: {list(drivers)}")

    return drivers
