<!--
 Copyright (C) 2022 Adam Kirchberger

 This file is part of Nectl.

 Nectl is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Nectl is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Nectl.  If not, see <http://www.gnu.org/licenses/>.
-->

# Drivers

## Summary

Drivers are used to enable communication between nectl and the end host. These are operating system specific and will use SDKs or API's provided by the host vendor.

The nectl core library includes some drivers but like all parts of nectl you are free to bring your own drivers (or override existing ones) in your network kit.

## Methods

Every driver implements the following methods

- `get_config`: pull active configuration into kit configs directory.
- `compare_config`: compare rendered staged config to active config and produce diff.
- `apply_config`: load staged config onto the host.

!> The paths used for configs can be overridden in your kit [settings file](guide/settings.md).

## Custom Drivers

Drivers are operating system specific and matched by using the driver filename and the value of the host `os_name` fact (just like templates).

Any custom drivers should be kept in your network kit and be version controlled.

A driver can be a single file or a directory (with an `__init__.py`) which contains a collection of files, this can be useful when building drivers where it makes sense to have separate files.

Nectl will look for custom drivers in `demo-kit/drivers` but this can overridden in your kit [settings file](guide/settings.md).

A default driver can be specified in your kit [settings file](guide/settings.md) to be used by hosts which do not match a core or kit driver. This can be useful when you want to fallback to a library like Napalm.

### Driver example

This is an example that can be used for building your own driver for an operating system named `nos`

<details>
<summary>Expand code block</summary>

```python
# demo-kit/drivers/nos.py

from nectl import BaseDriver


class NosDriver(BaseDriver):
    def __init__(
        self,
        host,
        username: str,
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
        super().__init__(
            host=host,
            username=username,
            password=password,
            ssh_private_key_file=ssh_private_key_file,
        )

        # Host SDK logic goes here
        self._driver = SDK(...)

    @property
    def is_connected(self) -> bool:
        """
        Returns True if successfully connected to host.

        Returns:
            bool: True if OK.
        """
        # Logic to check if self._driver is connected
        if self._driver.connected:
            return True
        return False

    def get_config(self, format: str = None, sanitized: bool = True) -> str:
        """
        Returns the active configuration from the host.

        Args:
            format (str): new config format.
            sanitized (bool): remove secret data.

        Returns:
            str: active config.
        """
        super().get_config(format)

        # Get config logic here
        config = self._driver.get_active()

        # Return config
        return config

    def compare_config(self, config_filepath: str, format: str = None) -> str:
        """
        Returns the configuration diff between the active and supplied config.

        Args:
            config_filepath (str): new config file.
            format (str): config format.

        Returns:
            str: active vs staged diff.
        """
        super().compare_config(config_filepath)

        # Get config and compare to content of `config_filepath`
        diff = self._driver.diff(config_filepath)

        # Return diff
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
            str: active vs staged diff.
        """
        super().apply_config(config_filepath)

        # Apply staged config to host
        diff = self._driver.push_config(config_filepath)

        # Return diff
        return diff

    def __enter__(self):
        """
        Open connection to host when context manager starts.
        """
        # Logic to establish connection to host using `self._driver`
        self._driver.connect()

        super().__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close connection to host when context manager finishes.
        """
        # Logic to close connection to host
        self._driver.close()

        super().__exit__(exc_type, exc_val, exc_tb)
```

</details>
