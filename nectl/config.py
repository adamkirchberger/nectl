import os
import json
from typing import List, Dict, Pattern, Optional
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

__config = None


class Config(BaseSettings):
    """
    Defines user configuration settings
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
    hosts_customer_regex: Optional[str] = None

    # Path to kit with datatree, models and templates
    kit_path: str

    # Datatree default directory name
    datatree_dirname: str = "data"

    # Templates default directory name
    templates_dirname: str = "templates"

    # Default data action
    default_action: str = "merge_with"

    @property
    def datatree_path(self):
        """
        Returns datapath tree using kit_path and datatree directory name
        """
        return os.path.join(self.kit_path, self.datatree_dirname)


def get_config() -> Config:
    """
    Return configuration.

    Returns:
        Config: config.
    """
    global __config
    if not __config:
        __config = load_config()

    return __config


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
