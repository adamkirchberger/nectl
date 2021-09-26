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

from os import getcwd
import time
from typing import Sequence, Dict, Any
import inspect

from ..logging import get_logger
from ..config import Config, get_config
from ..exceptions import (
    BlueprintImportError,
    BlueprintMissingError,
    RenderError,
)
from ..data.hosts import Host
from .blueprints import Blueprint, get_blueprint


logger = get_logger()


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

    blueprint_name = getattr(blueprint, "__name__")
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
            # Get args that template needs
            t_args = {}
            for arg_name, arg in inspect.signature(t).parameters.items():
                # Optional args which have default values
                if arg.default is not arg.empty:
                    t_args[arg_name] = facts.get(arg_name, arg.default)
                # Required args which will raise error when not in facts
                else:
                    t_args[arg_name] = facts[arg_name]

            # Render template
            render = t(**t_args)
        except KeyError as e:
            logger.critical(
                f"{host_id}: template '{blueprint_name}:{tname}' "
                f"needs fact: {str(e)}"
            )
            continue  # move to next template
        except Exception as e:
            logger.critical(
                f"{host_id}: template '{blueprint_name}:{tname}' unknown error: {e}"
            )
            logger.exception(e)
            continue  # move to next template
        out.append(render)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"{host_id}: finished render ({dur}s)")
    return "\n".join(out)
