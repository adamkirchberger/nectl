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

try:
    from pydantic import BaseSettings, ValidationError
except:
    from pydantic.v1 import BaseSettings, ValidationError

from . import __version__
from .exceptions import SettingsFileError

KIT_FILEPATH = os.getenv("NECTL_KIT", "./kit.py")

APP_VERSION = __version__
APP_DESCRIPTION = "Network control framework for network automation and orchestration."


class Settings(BaseSettings):
    """
    Defines kit configuration settings.
    """

    class Config:
        extra = "allow"

    # pylint: disable=R0902

    # Path to settings file
    settings_path: str

    # List of data inheritance lookup paths
    datatree_lookup_paths: List[str]

    # Glob pattern to find all hosts
    hosts_glob_pattern: str

    # Regex to determine host properties
    hosts_hostname_regex: str
    hosts_site_regex: Optional[str] = None
    hosts_customer_regex: Optional[str] = None

    # Path to kit with datatree, models and templates
    kit_path: str

    # Datatree default directory name
    datatree_dirname: str = "datatree"

    # Templates default directory name
    templates_dirname: str = "templates"

    # Checks default directory name
    checks_dirname: str = "checks"

    # Custom drivers directory name
    # Note that these will override library drivers if same name is used
    drivers_dirname: str = "drivers"

    # Default data action
    default_action: str = "replace_with"

    # Default rendered configs output directory
    staged_configs_dir: str = "configs/staged"

    # Default configs diffs directory
    config_diffs_dir: str = "configs/diffs"

    # Default active configs directory
    active_configs_dir: str = "configs/active"

    # Default configs file extension
    configs_file_extension: str = "txt"

    # Config format variable passed to driver methods
    configs_format: str = ""  # not in use

    # Defines whether configs pulled from devices should be sanitized
    configs_sanitized: bool = True

    # Defines a default driver if one is not found. Test and use at own risk!
    default_driver: str = ""

    # Check files/functions/classes must start with this value.
    # Classes use capitalized() value.
    checks_prefix: str = "check"

    # Default filename used for checks junit xml report.
    checks_report_filename: str = "nectl_checks.xml"

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
