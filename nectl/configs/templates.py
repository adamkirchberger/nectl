import os
import sys
import re
from importlib import import_module

from ..logging import get_logger
from ..config import Config, get_config
from ..exceptions import TemplateImportError, TemplateMissingError


logger = get_logger()


class Template(object):
    """
    Defines a template which is used to render host configurations.
    """


def get_template(os_name: str, os_version: str, config: Config = None) -> Template:
    """
    Returns the template based on the template map which uses host os and
    os_version to determine the template.

    Args:
        os_name (str): host operating system.
        os_version (str): host operating system version.
        config (Config): config settings.

    Returns:
        template module.

    Raises:
        TemplateMissingError: if host template cannot be determined.
        TemplateImportError: if template cannot be found or opened.
    """
    config = get_config() if config is None else config

    for bp_name, bp_match in config.templates_map.items():
        if re.match(bp_match.os_name_regex, os_name) and re.match(
            bp_match.os_version_regex, os_version
        ):
            return _import_template(
                bp_name,
                os.path.join(config.kit_path, config.templates_dirname),
            )

    raise TemplateMissingError(
        f"no template has matched host os_name='{os_name}' os_version='{os_version}'"
    )


def _import_template(name: str, templates_path: str) -> Template:
    """
    Imports a template module from a python file and returns it.

    Args:
        name (str): template file name. Example: 'foofile'
        templates_path (str): path to templates directory.

    Returns:
        template module.
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
        raise TemplateImportError(f"template '{mod_name}' error: {e}") from e

    except ModuleNotFoundError as e:
        raise TemplateImportError(f"template file not found: {mod_name}") from e

    return mod
