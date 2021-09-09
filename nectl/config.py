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
from typing import List, Dict, Pattern
import pkg_resources
import yaml
from pydantic import BaseSettings, validator
from pydantic.error_wrappers import ValidationError

from .exceptions import ConfigFileError

CONFIG_FILEPATH = os.getenv("NECTL_CONFIG", "~/.config/nectl_config")

try:
    APP_VERSION = pkg_resources.get_distribution("nectl").version
except pkg_resources.DistributionNotFound:
    APP_VERSION = "unknown"

APP_DESCRIPTION = "Network Control Tool"


class Config(BaseSettings):
    """
    Defines configuration settings
    """

    class Config:
        extra = "allow"

    # pylint: disable=R0902

    # Path to config file
    config_path: str

    # List of data inheritance lookup paths
    datatree_lookup_paths: List[str]

    # Glob pattern to find all hosts
    hosts_glob_pattern: str

    # Regex to determine host properties
    hosts_hostname_regex: str
    hosts_site_regex: str
    hosts_customer_regex: str

    # Path to kit with datatree, models and blueprints
    kit_path: str

    # Blueprint map matches hosts to blueprints using os and os_version regex
    class BlueprintMatchItem(BaseSettings):
        os_regex: Pattern
        os_version_regex: Pattern

    blueprints_map: Dict[str, BlueprintMatchItem] = {}

    # Datatree default directory name
    datatree_dirname: str = "data"

    # Blueprints default directory name
    blueprints_dirname: str = "blueprints"

    # Default data action
    default_action: str = "merge_with"

    @validator("blueprints_map")
    def blueprints_map_keys_must_have_module_and_class_name(cls, v):
        # pylint: disable=E0213,C0116,R0201
        for k in v.keys():
            if len(k.split(":")) != 2:
                raise ValueError("blueprints must be in format 'filename:ClassName'")

        return v

    @property
    def datatree_path(self):
        """
        Returns datapath tree using kit_path and datatree directory name
        """
        return os.path.join(self.kit_path, self.datatree_dirname)


def load_config(filepath: str = CONFIG_FILEPATH) -> Config:
    """
    Load external JSON or YAML config file.

    Args:
        filepath (str): path to config file.

    Returns:
        Config: loaded config.

    Raises:
        ConfigFileError: if an error is encountered with loading file.
    """
    if not isinstance(filepath, str):
        raise TypeError("filepath must be str")

    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            if filepath.endswith(".json"):
                config_args = json.load(fh)
            elif filepath.endswith(".yaml"):
                config_args = yaml.safe_load(fh)
            else:
                raise ConfigFileError("config file format must YAML or JSON.")
    except FileNotFoundError as e:
        raise ConfigFileError(f"config file not found '{filepath}'.") from e

    try:
        config = Config(
            kit_path=os.path.dirname(filepath), config_path=filepath, **config_args
        )
    except ValidationError as e:
        raise ConfigFileError(e) from e

        # raise ConfigFileError(
        #     "config file is missing variables or has invalid variable types"
        # ) from e

    return config
