import os
import sys
from importlib import import_module
from types import ModuleType

from ..logging import get_logger
from ..config import Config, get_config
from ..exceptions import TemplateImportError, TemplateMissingError


logger = get_logger()


Template = ModuleType  # Defines a template which is used to render host configurations.


def get_template(os_name: str, config: Config = None) -> Template:
    """
    Returns the template based on the host os_name value/

    Args:
        os_name (str): host operating system.
        config (Config): config settings.

    Returns:
        template module.

    Raises:
        TemplateMissingError: if host template cannot be found.
        TemplateImportError: if template exists but cannot opened.
    """
    config = get_config() if config is None else config

    return _import_template(
        name=os_name,
        templates_path=os.path.join(config.kit_path, config.templates_dirname),
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
        msg = f"template file not found matching os_name: {mod_name}"
        logger.critical(msg)
        logger.exception(e)
        raise TemplateMissingError(msg) from e

    return mod
