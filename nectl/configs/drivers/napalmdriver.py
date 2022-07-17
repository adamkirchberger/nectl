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


import json
import time
from napalm import get_network_driver
from napalm.base.base import NetworkDriver
from napalm.base.exceptions import (
    ModuleImportError,
    LockError,
    ConnectionException,
    MergeConfigException,
    ReplaceConfigException,
)
from ncclient.transport.errors import AuthenticationError


from ...logging import get_logger
from ...exceptions import (
    DriverError,
    DriverConfigLoadError,
    DriverCommitDisconnectError,
    DriverNotFoundError,
)
from ...datatree.hosts import Host
from . import BaseDriver
from .basedriver import COMMIT_COMMENT, COMMIT_WAIT_MULTIPLIER, CONNECT_TIMEOUT


logger = get_logger()


class NapalmDriver(BaseDriver):
    def __init__(
        self,
        host: Host,
        username: str = None,
        password: str = None,
        ssh_private_key_file: str = None,
    ) -> None:
        """
        Creates a host driver using the Napalm library. Napalm driver name is
        taken from the host's os_name fact.

        Args:
            host (Host): host instance.
            username (str): host username.
            password (str): host password.
            ssh_private_key_file (str): SSH private key file.
        """
        super().__init__(
            host=host,
            username=username,
            password=password,
            ssh_private_key_file=ssh_private_key_file,
        )

        # Set optional args for napalm
        self._optional_args = dict(
            key_file=ssh_private_key_file,
            auto_probe=CONNECT_TIMEOUT,  # (junos) - A timeout in seconds, for which to probe the device.
            config_lock=True,  # (iosxr_netconf, iosxr, junos) - Lock the config during open()
        )
        # Options can be added and overriden from datatree
        self._optional_args.update(host.facts.get("napalm_optional_args", {}))

        self._driver: NetworkDriver

    @property
    def is_connected(self) -> bool:
        if self._driver:
            return self._driver.is_alive().get("is_alive", False)
        return False

    def get_config(self, format: str = None, sanitized: bool = True) -> str:
        """
        Returns the active configuration from the host.

        Args:
            format (str): config format.
            sanitized (bool): remove secret data.

        Returns:
            str: active config.
        """
        super().get_config()
        return self._driver.get_config(retrieve="running", sanitized=sanitized).get(
            "running"
        )

    def compare_config(self, config_filepath: str, format: str = None) -> str:
        """
        Returns the configuration diff between the active and supplied config.

        Args:
            config_filepath (str): new config file.
            format (str): config format.

        Returns:
            str: config diff between active and supplied config file.

        Raises:
            DriverError: if there is a driver related issue.
            DriverConfigLoadError: if there is an issue loading config on host.
        """
        super().compare_config(config_filepath)
        # Run load config to check config and return diff with no commit
        diff = self._load_config(
            config_filepath=config_filepath, commit=False, commit_timer=0
        )
        return diff

    def apply_config(
        self, config_filepath: str, format: str = None, commit_timer: int = 1
    ) -> str:
        """
         Apply staged config onto host.

        Args:
            config_filepath (str): new config file.
            format (str): config format.
            commit_timer (int): automatic rollback in minutes. Defaults to 1.

        Returns:
            str: config diff between active and supplied config file.

        Raises:
            DriverError: if there is a driver related issue.
            DriverConfigLoadError: if there is an issue loading config on host.
            DriverCommitDisconnectError: if connection is lost after commit.
        """
        super().apply_config(config_filepath)
        # Run load config to check config, commit with timer and return diff.
        diff = self._load_config(
            config_filepath=config_filepath,
            commit=True,
            commit_timer=commit_timer,
        )
        return diff

    def _load_config(
        self,
        config_filepath: str,
        commit_timer: int,
        commit: bool = False,
    ):
        """
        Loads config onto host to test if config is valid, commits if requested
        and returns diff.

        Args:
            config_filepath (str): new config file.
            commit_timer (int): automatic rollback in minutes if connection lost.
            commit (bool): if True will commit config to host. Defaults to False.

        Returns:
            str: config diff between active and supplied config file.

        Raises:
            DriverError: if there is a driver related issue.
            DriverConfigLoadError: if there is an issue loading config on host.
            DriverCommitDisconnectError: if connection is lost after commit.
        """
        diff = None

        try:
            # Open new config file
            with open(config_filepath, "r", encoding="utf-8") as fh:
                config = fh.read()

            # Load and compare config
            if self.host.os_name == "junos" and config.strip().split(" ")[0] == "set":
                # Junos specific logic when config in `set` format
                logger.debug(
                    f"[{self.host.id}] host is junos using 'set' config format"
                )
                # Junos workaround will delete candidate config first
                self._driver.load_merge_candidate(config="delete")
                # and then merge using the set commands
                self._driver.load_merge_candidate(config=config)

            else:
                # All other devices and formats use Napam's replace
                self._driver.load_replace_candidate(config=config)

            # Get config diff
            diff = self._driver.compare_config()
            logger.debug(f"[{self.host.id}] config check passed")

        except FileNotFoundError as e:
            raise DriverConfigLoadError(
                f"config file not found: {config_filepath}"
            ) from e
        except (ReplaceConfigException, MergeConfigException) as e:
            msg = "host rejected config due to errors:\n"
            # Append all error messages
            msg += json.dumps(e.args, indent=4, default=str)
            raise DriverConfigLoadError(msg) from e

        # No diff skip commit
        if not diff:
            logger.info(f"[{self.host.id}] no changes skipping")

        # No commit, diff only
        elif commit is False:
            logger.info(f"[{self.host.id}] has changes but not comitting")

        # Commit requested
        elif commit is True:
            logger.info(
                f"[{self.host.id}] config committed with {commit_timer} "
                "minutes automatic rollback"
            )

            try:
                # Commit config
                self._driver.commit_config(
                    message=COMMIT_COMMENT if self.host.os_name != "eos" else "",
                    revert_in=max(60, commit_timer * 60),  # 1 minute minimum
                )
                # Restart connection to validate mgmt access post commit
                logger.debug(f"[{self.host.id}] restarting connection")
                self.__enter__()
                logger.info(f"[{self.host.id}] restarted connection")

            except Exception as e:
                raise DriverCommitDisconnectError(
                    "host connection lost after commit: "
                    f"{e.__class__.__name__}: {e}",
                    diff=diff,
                ) from e

            # Wait for 75% of commit timer
            sleep_mins = commit_timer * COMMIT_WAIT_MULTIPLIER
            logger.info(
                f"[{self.host.id}] waiting {sleep_mins} minutes for config to settle"
            )
            time.sleep(sleep_mins * 60)

            # Confirm previous commit
            self._driver.confirm_commit()
            logger.info(f"[{self.host.id}] config commit confirmed")

        return diff

    def __enter__(self):
        """
        Open connection to host when context manager starts.
        """
        logger.debug(f"[{self.host.id}] opening connection to host")
        try:
            self._driver: NetworkDriver = get_network_driver(self.host.os_name)(
                hostname=self.host.mgmt_ip,
                username=self.username,
                password=self.password,
                timeout=5,
                optional_args=self._optional_args,
            )
            self._driver.open()
        except ModuleImportError as e:
            raise DriverNotFoundError(
                "napalm driver '{self.host.os_name}' not found: {e}"
            ) from e
        except LockError as e:
            raise DriverError(
                "failed to take lock ensure no user in config mode"
            ) from e
        except AuthenticationError as e:
            raise DriverError(f"host reachable but authentication failed: {e}") from e
        except ConnectionException as e:
            raise DriverError(f"connection failed host is unreachable: {e}") from e

        super().__enter__()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close connection to host when context manager finishes.
        """
        logger.debug(f"[{self.host.id}] closing connection to host")
        try:
            self._driver.close()
        except Exception as e:
            logger.warning(
                f"[{self.host.id}] error closing connection: {e.__class__.__name__}: {e}"
            )
        super().__exit__(exc_type, exc_val, exc_tb)
