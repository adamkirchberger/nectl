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

import abc
from os import getenv

from ...logging import get_logger
from ...exceptions import DriverError, DriverNotConnectedError
from ...datatree.hosts import Host

COMMIT_COMMENT = getenv("NECTL_COMMIT_COMMENT", "Configured by Nectl.")
COMMIT_WAIT_MULTIPLIER = 0.75
CONNECT_TIMEOUT = 5
logger = get_logger()


def ensure_connected(func):
    """
    Wrapper used around methods which must only run when host is connected.
    """

    def ensure_connected_wrapper(self, *args, **kwargs):
        if not self.is_connected:
            raise DriverNotConnectedError(
                f"'{func.__name__}' must be run within context manager"
            )
        func(self, *args, **kwargs)

    return ensure_connected_wrapper


class BaseDriver(metaclass=abc.ABCMeta):
    def __init__(
        self,
        host: Host,
        username: str = None,
        password: str = None,
        ssh_private_key_file: str = None,
    ) -> None:
        """
        Interface for a NOS specific driver used to configure a host.
        Drivers use a context manager to open and close connection.

        Args:
            host (Host): host instance.
            username (str): host username.
            password (str): host password.
            ssh_private_key (str): SSH private key file.
        """
        self.host = host
        self.username = username if username else self.host.username
        self.password = password if password else self.host.password
        self.ssh_private_key_file = ssh_private_key_file
        self._driver = None

        if not self.host.mgmt_ip:
            raise DriverError("host has no mgmt_ip")

    @property
    @abc.abstractmethod
    def is_connected(self) -> bool:
        """
        Returns True if successfully connected to host.

        Returns:
            bool: True if OK.
        """

    @abc.abstractmethod
    @ensure_connected
    def get_config(self, format: str = None, sanitized: bool = True) -> str:
        """
        Returns the active configuration from the host.

        Args:
            format (str): new config format.
            sanitized (bool): remove secret data.

        Returns:
            str: active config.
        """

    @abc.abstractmethod
    @ensure_connected
    def compare_config(self, config_filepath: str, format: str = None) -> str:
        """
        Returns the configuration diff between the active and supplied config.

        Args:
            config_filepath (str): new config file.
            format (str): config format.

        Returns:
            str: active vs staged diff.
        """

    @abc.abstractmethod
    @ensure_connected
    def apply_config(
        self, config_filepath: str, format: str = None, commit_timer: int = 1
    ) -> str:
        """
        Apply staged config onto host.

        Args:
            config_filepath (str): new config file.
            format (str): optional config format.
            commit_timer (int): automatic rollback in minutes. Defaults to 1.

        Returns:
            str: active vs staged diff.
        """

    @abc.abstractmethod
    def __enter__(self):
        """
        Open connection to host when context manager starts.
        """
        logger.debug(f"[{self.host.id}] opened connection")
        return self

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close connection to host when context manager finishes.
        """
        logger.debug(f"[{self.host.id}] closed connection")
