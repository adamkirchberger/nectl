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

# pylint: disable=E1101

import time
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import (
    ConnectRefusedError,
    ProbeError,
    LockError,
    UnlockError,
    ConfigLoadError,
    CommitError,
    RpcTimeoutError,
    ConnectAuthError,
)

from ...logging import get_logger
from ...exceptions import (
    DriverError,
    DriverConfigLoadError,
    DriverCommitDisconnectError,
)
from ...datatree.hosts import Host
from . import BaseDriver
from .basedriver import COMMIT_COMMENT

Device.auto_probe = 3  # probe host for reachability before establishing
logger = get_logger()


class JunosDriver(BaseDriver):
    def __init__(
        self,
        host: Host,
        username: str = None,
        password: str = None,
        ssh_private_key_file: str = None,
    ) -> None:
        """
        Creates a Juniper Junos host driver.

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

        self._driver: Device = Device(
            host=self.host.mgmt_ip,
            user=self.username,
            passwd=self.password,
            ssh_private_key_file=self.ssh_private_key_file,
            timeout=5,
            attempts=1,
            gather_facts=False,
        )

        self._driver.bind(cu=Config)

    @property
    def is_connected(self) -> bool:
        return self._driver.connected

    def get_config(self, format="set") -> str:
        """
        Returns the active configuration from the host.

        Args:
            format (str): Junos config format. Defaults to "set".

        Returns:
            str: active config.
        """
        super().get_config()
        rpc_reply = self._driver.rpc.get_config(
            options={"format": format},
        )

        return rpc_reply.text

    def compare_config(self, config_filepath: str, format: str = "set") -> str:
        """
        Returns the configuration diff between the active and supplied config.

        Args:
            config_filepath (str): new config file.
            format (str): Junos config format. Defaults to "set".

        Returns:
            str: config diff between active and supplied config file.

        Raises:
            DriverError: if there is a driver related issue.
            DriverConfigLoadError: if there is an issue loading config on host.
        """
        super().compare_config(config_filepath)
        # Run load config to check config and return diff with no commit
        diff = self._load_config(
            config_filepath=config_filepath, format=format, commit=False
        )
        return diff

    def apply_config(
        self, config_filepath: str, format: str = "set", commit_timer: int = 1
    ) -> str:
        """
         Apply staged config onto host.

        Args:
            config_filepath (str): new config file.
            format (str): Junos config format. Defaults to "set".
            commit_timer (int): automatic rollback in minutes if connection lost. Defaults to 1.

        Returns:
            str: config diff between active and supplied config file.
        """
        super().apply_config(config_filepath)
        # Run load config to check config, commit with timer and return diff.
        diff = self._load_config(
            config_filepath=config_filepath,
            format=format,
            commit=True,
            commit_timer=commit_timer,
        )
        return diff

    def _load_config(
        self,
        config_filepath: str,
        format="set",
        commit=False,
        commit_timer=2,
    ):
        """
        Loads config onto host to test if config is valid, commits if requested
        and returns diff.

        Args:
            config_filepath (str): new config file.
            format (str): Junos config format. Defaults to "set".
            commit (bool): if True will commit config to host. Defaults to False.
            commit_timer (str): automatic rollback in minutes if connection lost. Defaults to 2.

        Returns:
            str: config diff between active and supplied config file.

        Raises:
            DriverError: if there is a driver related issue.
            DriverConfigLoadError: if there is an issue loading config on host.
        """
        diff = None

        try:
            # Obtain config lock on device
            self._driver.cu.lock()
            logger.debug(f"[{self.host.id}] took config lock")

            # Set format uses merge with an initial delete to replace config
            if format == "set":
                self._driver.cu.load("delete", format="set", merge=True)
                self._driver.cu.load(
                    path=config_filepath,
                    format="set",
                    merge=True,
                )
            # Other formats use update to replace config
            else:
                self._driver.cu.load(path=config_filepath, update=True)

            # Check commit
            self._driver.cu.commit_check()
            logger.debug(f"[{self.host.id}] config check passed")

            # Get config diff
            diff = self._driver.cu.diff()

            # No diff skip commit
            if diff is None:
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
                self._driver.cu.commit(
                    comment=COMMIT_COMMENT,
                    confirm=max(1, commit_timer),  # 1 minute minimum
                    timeout=5,
                )

                # Restart connection to validate mgmt access post commit
                logger.debug(f"[{self.host.id}] restarting connection")
                self._driver.close()
                self.__enter__()
                logger.info(f"[{self.host.id}] restarted connection")

                # Wait for 75% of commit timer
                sleep_mins = commit_timer * 0.75
                logger.info(
                    f"[{self.host.id}] waiting {sleep_mins} minutes for config "
                    "to settle"
                )
                time.sleep(sleep_mins * 60)

                # Confirm previous commit
                self._driver.cu.commit_check()
                logger.info(f"[{self.host.id}] config commit confirmed")

            # Unlock
            logger.debug(f"[{self.host.id}] released config lock")

        except (LockError, UnlockError) as e:
            raise DriverError(
                "failed to take lock ensure no user in config mode"
            ) from e
        except FileNotFoundError as e:
            raise DriverConfigLoadError(
                f"config file not found: {config_filepath}"
            ) from e
        except (ConfigLoadError, CommitError) as e:
            msg = f"host rejected config due to {len(e.errs)} errors:\n"
            # Append all error messages with useful info
            for i, er in enumerate(e.errs):
                msg += (
                    (f"{i+1}:\n")
                    + (
                        f"  path: {er.get('edit_path')}\n"
                        if er.get("edit_path")
                        else ""
                    )
                    + (
                        f"  element: '{er.get('bad_element')}'\n"
                        if er.get("bad_element")
                        else ""
                    )
                    + f"  error: {er.get('message')}\n"
                )
            raise DriverConfigLoadError(msg) from e
        except (RpcTimeoutError, ConnectAuthError) as e:
            raise DriverCommitDisconnectError(
                "host connection lost after commit", diff=diff
            ) from e

        return diff

    def __enter__(self):
        """
        Open connection to host when context manager starts.
        """
        logger.debug(f"[{self.host.id}] opening connection to host")
        try:
            self._driver.open()
            try:
                self._driver.timeout = 5
                self._driver._conn._session.transport.set_keepalive(2)
            except AttributeError:
                pass
        except ConnectRefusedError as e:
            raise DriverError(
                f"host reachable but NETCONF connection failed: {e}"
            ) from e
        except ConnectAuthError as e:
            raise DriverError(f"host reachable but authentication failed: {e}") from e
        except ProbeError as e:
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
        except RpcTimeoutError:
            pass
        super().__exit__(exc_type, exc_val, exc_tb)
