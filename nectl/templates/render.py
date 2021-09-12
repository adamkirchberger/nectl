from os import getcwd
import time
from typing import Sequence, Dict, Any

from ..logging import logger
from ..config import Config, get_config
from ..exceptions import (
    BlueprintImportError,
    BlueprintMissingError,
    RenderError,
)
from ..data.hosts import Host
from .blueprints import Blueprint, get_blueprint


def render_hosts(
    hosts: Sequence[Host], config: Config = get_config()
) -> Dict[str, Any]:
    """
    Returns templates for host which have been rendered using blueprints which
    are matched on 'os_name' and 'os_version' using the 'blueprints_map' var.

    Args:
        hosts (List[Host]): hosts to render templates for.
        config (Config): config settings.

    Returns:
        Dict[str,Any]: dict with item per host with rendered template.

    Raises:
        RenderError: if there are issues with blueprints or templates.
    """
    if not config.blueprints_map:
        raise RenderError(
            "templates cannot be rendered when 'blueprints_map' is not defined."
        )

    results = {}

    ts_start = time.perf_counter()
    logger.debug("start rendering templates")

    for host in hosts:
        print(host)
        print(host.os_name)
        if host.os_name is None or host.os_version is None:
            logger.info(
                f"skipping host render with no 'os_name' or 'os_version': {host.id}"
            )
            continue

        try:
            # Get matching blueprint
            blueprint = get_blueprint(host.os_name, host.os_version, config=config)
        except (BlueprintMissingError, BlueprintImportError) as e:
            raise RenderError(str(e)) from e
        except Exception as e:
            logger.exception(e)
            raise RenderError(f"unknown error: {e}") from e

        results[host.id] = render_blueprint(blueprint, host.facts)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished rendering templates ({dur}s)")

    return results


def render_blueprint(blueprint: Blueprint, facts: Dict[str, Any]) -> str:
    """
    Returns rendered configuration for host facts using supplied blueprint.

    Args:
        blueprint: Template blueprint class.
        facts (Dict[str,Any]): host facts.

    Returns:
        rendered host configuration.
    """
    ts_start = time.perf_counter()
    host_id = facts.get("id")
    logger.debug(f"{host_id}: starting render")

    blueprint_name = type(blueprint).__name__
    logger.info(f"{host_id}: using blueprint '{blueprint_name}'")

    logger.debug(f"{host_id}: collecting blueprint templates")
    templates = {
        t: getattr(blueprint, t)
        for t in dir(blueprint)
        if callable(getattr(blueprint, t)) and not t.startswith("_")
    }
    logger.debug(
        f"{host_id}: found {len(templates)} templates: {list(templates.keys())}"
    )

    out = []

    for tname, t in templates.items():
        logger.info(f"{host_id}: rendering template: {blueprint_name}:{tname}")
        try:
            render = t(**facts)
        except TypeError as e:
            if "missing" in str(e):
                logger.critical(
                    f"{host_id}: template '{blueprint_name}:{tname}' "
                    f"needs fact: {str(e).split(': ')[1]}"
                )
            else:
                logger.critical(
                    f"{host_id}: template '{blueprint_name}:{tname}' " f": {e}"
                )
            logger.exception(e)
            continue
        out.append(render)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"{host_id}: finished render ({dur}s)")
    return "\n".join(out)
