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
import re
from pydoc import locate, ErrorDuringImport

from ..logging import logger
from ..config import Config
from ..exceptions import BlueprintImportError, BlueprintMissingError
from ..models import BaseBlueprint


def get_blueprint(config: Config, host_os: str, host_os_version: str) -> BaseBlueprint:
    """
    Returns the blueprint based on the blueprint map which uses host os and
    os_version to determine the blueprint.

    Args:
        config (Config): config settings.
        host_os (str): host operating system.
        host_os_version (str): host operating system version.

    Returns:
        blueprint class.

    Raises:
        BlueprintMissingError: if host blueprint cannot be determined.
        BlueprintImportError: if blueprint cannot be found or opened.
    """
    for bp_name, bp_match in config.blueprints_map.items():
        if re.match(bp_match.os_regex, host_os) and re.match(
            bp_match.os_version_regex, host_os_version
        ):
            return _import_blueprint(
                bp_name,
                os.path.join(config.kit_path, config.blueprints_dirname),
            )

    raise BlueprintMissingError(
        f"no blueprint has matched host os='{host_os}' os_version='{host_os_version}'"
    )


def _import_blueprint(name: str, blueprints_path: str) -> BaseBlueprint:
    """
    Imports a blueprint class from a python file and returns it.

    Args:
        name (str): blueprint name with class name. Example: 'foofile:FooClass'
        blueprints_path (str): path to blueprints directory.

    Returns:
        blueprint class.
    """
    # Append path to pythonpath
    if blueprints_path not in sys.path:
        logger.debug(f"appending blueprints to PYTHONPATH: {blueprints_path}")
        sys.path.insert(0, blueprints_path)

    mod_name, class_name = name.split(":")
    mod_name = mod_name.replace("/", ".")
    logger.debug(f"importing blueprint module='{mod_name}' class='{class_name}'")

    try:
        # Get blueprint module
        mod = locate(mod_name)
    except ErrorDuringImport as e:
        raise BlueprintImportError(f"blueprint '{mod_name}' has errors: {e}") from e

    if not mod:
        raise BlueprintImportError(f"blueprint file not found: {mod_name}")

    try:
        # Get blueprint class
        return getattr(mod, class_name)
    except AttributeError as e:
        raise BlueprintImportError(
            f"blueprint '{mod_name}' class not found named: {class_name}"
        ) from e
