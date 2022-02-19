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

"""
Template related discovery and import functions.
"""
import os
import sys
from importlib import import_module
from types import ModuleType

from ..logging import get_logger
from ..settings import Settings
from ..exceptions import TemplateImportError, TemplateMissingError


logger = get_logger()


Template = ModuleType  # Defines a template which is used to render host configurations.


def get_template(settings: Settings, os_name: str) -> Template:
    """
    Returns the template based on the host os_name value/

    Args:
        settings (Settings): config settings.
        os_name (str): host operating system.

    Returns:
        template module.

    Raises:
        TemplateMissingError: if host template cannot be found.
        TemplateImportError: if template exists but cannot opened.
    """
    return _import_template(
        name=os_name,
        templates_path=os.path.join(settings.kit_path, settings.templates_dirname),
    )


def _import_template(name: str, templates_path: str) -> Template:
    """
    Imports a template module from a python file and returns it.

    Args:
        name (str): template file name. Example: 'foofile'
        templates_path (str): path to templates directory.

    Returns:
        template module.

    Raises:
        TemplateMissingError: if host template cannot be found.
        TemplateImportError: if template exists but cannot opened.
    """
    # Append path to pythonpath
    if templates_path not in sys.path:
        logger.debug(f"appending templates to PYTHONPATH: {templates_path}")
        sys.path.insert(0, templates_path)

    mod_name = name.replace("/", ".")
    logger.debug(f"importing template module='{mod_name}'")

    try:
        # Get template module
        mod = import_module(mod_name)

        # Force reimport when reused for another host
        del sys.modules[mod_name]

    except SyntaxError as e:
        msg = f"template for os_name '{mod_name}' has error: {e}"
        logger.critical(msg)
        logger.exception(e)
        raise TemplateImportError(msg) from e

    except ModuleNotFoundError as e:
        msg = f"template import error with os_name: {mod_name}"
        logger.critical(msg)
        logger.exception(e)
        raise TemplateMissingError(msg) from e

    return mod
