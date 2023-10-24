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

import time
from typing import List, Tuple, Type, Dict, Optional, Any, Literal

from ...logging import get_logger
from ...settings import Settings
from ...exceptions import (
    DriverNotFoundError,
    DriverCommitDisconnectError,
    DriverError,
    DriverConfigLoadError,
)
from ..utils import write_configs_to_dir
from .utils import load_drivers_from_kit
from .basedriver import BaseDriver
from .napalmdriver import NapalmDriver
from ...datatree.hosts import Host

logger = get_logger()


class Drivers:
    """
    Map os_name to drivers.
    """

    core_drivers = {"junos": NapalmDriver, "eos": NapalmDriver}
    kit_drivers: Optional[dict] = None


def get_driver(settings: Settings, os_name: str) -> Type[BaseDriver]:
    """
    Returns the driver from the supplied os_name if one can be found. Checks
    drivers in kit followed by core drivers.

    Args:
        settings (Settings): config settings.
        os_name (str): host OS name.

    Returns:
        BaseDriver: driver object.
    """
    if not Drivers.kit_drivers:
        # Load kit drivers once
        Drivers.kit_drivers = load_drivers_from_kit(settings)

    # Lookup custom drivers in kit
    logger.debug(f"checking kit drivers for os_name: {os_name}")
    for driver_os_name, driver in Drivers.kit_drivers.items():
        if os_name == driver_os_name:
            return driver

    # Lookup core drivers
    logger.debug(f"checking core drivers for os_name: {os_name}")
    for driver_os_name, driver in Drivers.core_drivers.items():
        if os_name == driver_os_name:
            return driver

    # Use a default driver
    logger.debug("checking if default driver is defined")
    if settings.default_driver:
        if settings.default_driver == "napalm":
            return NapalmDriver

        # Default driver does not exist
        raise DriverNotFoundError(
            f"no default driver found matching name: {settings.default_driver}"
        )

    raise DriverNotFoundError(f"no driver found that matches os_name: {os_name}")


def run_driver_method_on_hosts(
    settings: Settings,
    hosts: List[Host],
    method_name: Literal["compare_config", "apply_config", "get_config"],
    description: str,
    username: Optional[str] = None,
    password: Optional[str] = None,
    ssh_private_key_file: Optional[str] = None,
) -> Tuple[int, Dict[str, Any]]:
    """
    Runs specified driver method on all supplied hosts. Driver method should be
    one of "compare_config", "apply_config" or "get_config".

    Args:
        settings (Settings): config settings.
        hosts (List[Host]): list of hosts to run method against.
        method_name (str): name of driver method.
        description (str): action description used in log outputs.
        username (str): override host username.
        password (str): override host password.
        ssh_private_key_file (str): override ssh private key file.

    Returns:
        Tuple(int, Dict[str, Any]): total errors and dict with host.id and outputs.
    """
    host_outputs = {}
    errors = 0

    ts_start = time.perf_counter()
    logger.debug(f"start {description}")

    for host in hosts:
        # Skip hosts with no os_name or mgmt_ip
        if not host.os_name or not host.mgmt_ip:
            logger.warning(
                f"[{host.id}] skipping due to missing 'os_name' or 'mgmt_ip'"
            )
            continue

        # Create host driver
        try:
            driver = get_driver(settings=settings, os_name=host.os_name)(
                host=host,
                username=username if username else host.username,
                password=password if password else host.password,
                ssh_private_key_file=ssh_private_key_file,
            )
        except (DriverNotFoundError, DriverError) as e:
            logger.error(f"[{host.id}] {e}")
            errors += 1
            continue  # skip host

        # Prepare args
        kwargs: Dict[str, Any] = {}
        if method_name in ["compare_config", "apply_config"]:
            kwargs["config_filepath"] = (
                f"{settings.kit_path}/{settings.staged_configs_dir}/"
                + f"{host.id}.{settings.configs_file_extension}"
            )
        elif method_name == "get_config":
            kwargs["format"] = settings.configs_format
            kwargs["sanitized"] = settings.configs_sanitized

        # Open connection to host
        try:
            with driver as con:
                logger.info(f"[{host.id}] opened connection to host")
                # Run method with host and store output
                output = getattr(con, method_name)(**kwargs)
            logger.info(f"[{host.id}] closed connection to host")

            # Update dict to hold output results indexed by host id
            host_outputs.update({host.id: output})

        except (DriverError, DriverConfigLoadError, DriverCommitDisconnectError) as e:
            logger.error(f"[{host.id}] {e}")
            errors += 1

            if isinstance(e, DriverCommitDisconnectError):
                # Update with commit diff that caused disconnect
                host_outputs.update({host.id: e.diff})

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished {description} ({dur}s)")

    return (errors, host_outputs)
