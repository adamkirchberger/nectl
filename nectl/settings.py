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
import json
from typing import List, Optional
import pkg_resources
import yaml
from pydantic import BaseSettings, ValidationError

from .exceptions import SettingsFileError

SETTINGS_FILEPATH = os.getenv(
    "NECTL_SETTINGS", os.getenv("NECTL_CONFIG", "./nectl.yaml")
)

try:
    APP_VERSION = pkg_resources.get_distribution("nectl").version
except pkg_resources.DistributionNotFound:
    APP_VERSION = "unknown"

APP_DESCRIPTION = "Network Control Tool"


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
    datatree_dirname: str = "data"

    # Templates default directory name
    templates_dirname: str = "templates"

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


def load_settings(filepath: str = SETTINGS_FILEPATH) -> Settings:
    """
    Load external JSON or YAML settings file.

    Args:
        filepath (str): path to settings file.

    Returns:
        Settings: kit settings.

    Raises:
        SettingsFileError: if an error is encountered with loading file.
    """
    if not isinstance(filepath, str):
        raise TypeError("filepath must be str")

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            if filepath.endswith(".json"):
                opts = json.load(fh)
            elif filepath.endswith(".yaml"):
                opts = yaml.safe_load(fh)
            else:
                raise SettingsFileError("settings file format must YAML or JSON")
    except FileNotFoundError as e:
        raise SettingsFileError(f"settings file not found '{filepath}'") from e

    try:
        settings = Settings(
            kit_path=os.path.dirname(filepath), settings_path=filepath, **opts
        )
    except ValidationError as e:
        raise SettingsFileError(e) from e

    return settings
