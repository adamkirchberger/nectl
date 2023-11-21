# Copyright (C) 2021 Adam Kirchberger
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

from typing import Optional


class DiscoveryError(Exception):
    """
    Indicates that an error has been encountered during data tree discovery.
    """


class SettingsFileError(Exception):
    """
    Indicates that errors have been encountered related to settings file.
    """


class RenderError(Exception):
    """
    Indicates that render of hosts has encountered an error.
    """


class TemplateMissingError(Exception):
    """
    Indicates that no suitable template has been found for host.
    """


class TemplateImportError(Exception):
    """
    Indicates that template file does not exist or has errors.
    """


class DriverNotFoundError(Exception):
    """
    Indicates that a matching driver can not be found for the host.
    """


class DriverLoadError(Exception):
    """
    Indicates that an error was encountered when loading a custom kit driver.
    """


class DriverError(Exception):
    """
    Indicates that an error has been encountered by the host driver.
    """


class DriverNotConnectedError(Exception):
    """
    Indicates that a driver method has been run with no connection to host.
    """


class DriverConfigLoadError(Exception):
    """
    Indicates that errors have been encountered when loading config to host.
    """


class DriverCommitDisconnectError(Exception):
    """
    Indicates that a host disconnected after commit most likely from bad config.

    Args:
        diff (str): commit diff before disconnect.
    """

    def __init__(self, *args: object, diff: Optional[str] = None) -> None:
        super().__init__(*args)
        self.diff = diff


class ChecksError(Exception):
    """
    Indicates that an error has been encountered during checks execution.
    """
