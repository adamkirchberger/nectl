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

import os
import sys
from typing import List, Optional
from importlib import import_module

from pydantic import Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from . import __version__
from .exceptions import SettingsFileError

KIT_FILEPATH = os.getenv("NECTL_KIT", "./kit.py")

APP_VERSION = __version__
APP_DESCRIPTION = "Network control framework for network automation and orchestration."


class Settings(BaseSettings):
    """
    Defines kit configuration settings.
    """

    model_config = SettingsConfigDict(extra="allow")

    # pylint: disable=R0902

    settings_path: str = Field(description="Path to settings file")

    datatree_lookup_paths: List[str] = Field(
        description="List of data inheritance lookup paths"
    )

    hosts_glob_pattern: str = Field(description="Glob pattern to find all hosts")

    hosts_hostname_regex: str = Field(description="Regex to determine host hostname")
    hosts_site_regex: Optional[str] = Field(
        default=None, description="Regex to determine host site"
    )
    hosts_customer_regex: Optional[str] = Field(
        default=None, description="Regex to determine host customer"
    )

    kit_path: str = Field(description="Path to kit with datatree, models and templates")

    datatree_dirname: str = Field(
        default="datatree", description="Datatree default directory name"
    )

    templates_dirname: str = Field(
        default="templates", description="Templates default directory name"
    )

    checks_dirname: str = Field(
        default="checks", description="Checks default directory name"
    )

    drivers_dirname: str = Field(
        default="drivers",
        description="Custom drivers directory name (will override library drivers if same name is used)",
    )

    default_action: str = Field(default="replace_with", description="Default data action")

    staged_configs_dir: str = Field(
        default="configs/staged", description="Default rendered configs output directory"
    )

    config_diffs_dir: str = Field(
        default="configs/diffs", description="Default configs diffs directory"
    )

    active_configs_dir: str = Field(
        default="configs/active", description="Default active configs directory"
    )

    configs_file_extension: str = Field(
        default="txt", description="Default configs file extension"
    )

    configs_format: str = Field(
        default="", description="Config format variable passed to driver methods"
    )

    configs_sanitized: bool = Field(
        default=True,
        description="Defines whether configs pulled from devices should be sanitized",
    )

    default_driver: str = Field(
        default="",
        description="Defines a default driver if one is not found (test and use at own risk)",
    )

    checks_prefix: str = Field(
        default="check",
        description="Check files/functions/classes must start with this value (classes use capitalized value)",
    )

    checks_report_filename: str = Field(
        default="nectl_checks.xml",
        description="Default filename used for checks junit xml report",
    )

    @property
    def datatree_path(self) -> str:
        """
        Returns datapath tree using kit_path and datatree directory name
        """
        return os.path.join(self.kit_path, self.datatree_dirname)


def get_settings() -> Settings:
    """
    Return kit settings.

    Returns:
        Settings: kit settings.
    """
    return load_settings()


def load_settings(filepath: Optional[str] = KIT_FILEPATH) -> Settings:
    """
    Load kit settings file.

    Args:
        filepath (str): path to settings file.

    Returns:
        Settings: kit settings.

    Raises:
        SettingsFileError: if an error is encountered with loading file.
    """
    if not isinstance(filepath, str):
        raise TypeError("filepath must be str")

    if not filepath.endswith(".py"):
        raise SettingsFileError("settings file must have '.py' extension")

    try:
        # Append kit to pythonpath
        kit_path = os.path.dirname(filepath)
        if kit_path not in sys.path:
            sys.path.insert(0, kit_path)

        # Extract keys and values from settings file
        opts = {
            k: v
            for k, v in import_module(
                os.path.splitext(os.path.basename(filepath))[
                    0
                ]  # get filename without path and extension
            ).__dict__.items()
            if not k.startswith("_")
        }

    except ModuleNotFoundError as e:
        raise SettingsFileError(f"settings file not found '{filepath}'") from e

    except SyntaxError as e:
        raise SettingsFileError(f"settings file is not valid: {e}") from e

    try:
        settings = Settings(kit_path=kit_path, settings_path=filepath, **opts)
    except ValidationError as e:
        raise SettingsFileError(e) from e

    return settings
