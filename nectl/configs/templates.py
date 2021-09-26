import os
import sys
import re
from pydoc import locate, ErrorDuringImport

from ..logging import get_logger
from ..config import Config, get_config
from ..exceptions import TemplateImportError, TemplateMissingError


logger = get_logger()


class Template:
    """
    Defines class for a template which is used to render host configurations.
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
        template class.

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
    Imports a template class from a python file and returns it.

    Args:
        name (str): template name with class name. Example: 'foofile:FooClass'
        templates_path (str): path to templates directory.

    Returns:
        template class.
    """
    # Append path to pythonpath
    if templates_path not in sys.path:
        logger.debug(f"appending templates to PYTHONPATH: {templates_path}")
        sys.path.insert(0, templates_path)

    mod_name, class_name = name.split(":")
    mod_name = mod_name.replace("/", ".")
    logger.debug(f"importing template module='{mod_name}' class='{class_name}'")

    try:
        # Get template module
        mod = locate(mod_name)
    except ErrorDuringImport as e:
        raise TemplateImportError(f"template '{mod_name}' has errors: {e}") from e

    if not mod:
        raise TemplateImportError(f"template file not found: {mod_name}")

    try:
        # Get template class
        return getattr(mod, class_name)
    except AttributeError as e:
        raise TemplateImportError(
            f"template '{mod_name}' class not found named: {class_name}"
        ) from e
