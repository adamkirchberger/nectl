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
Fact loading functions.
"""
import sys
import json
import time
import importlib
import pkgutil
from types import ModuleType
from typing import List, Dict, TYPE_CHECKING
from enum import Enum
from ipaddress import IPv4Interface
from pydantic import BaseModel
from dpath import util as merge_utils

from ..logging import get_logger
from ..config import Config
from .actions import Actions, DEFAULT_ACTION

if TYPE_CHECKING:
    from .hosts import Host

VALID_DATA_TYPES = (list, dict, str, int, float)
MERGE_TYPE = merge_utils.MERGE_ADDITIVE
logger = get_logger()


def get_facts_for_hosts(
    config: Config,
    hosts: List["Host"],
) -> Dict[str, Dict]:
    """
    Returns a dict of facts loaded from datatree for each provided host.

    Args:
        config (Config): config settings.
        hosts (List[BaseHost]): list of hosts.

    Returns:
        Dict[str,Dict]: one item per unique host with loaded facts.
    """
    facts = {}

    ts_start = time.perf_counter()
    logger.debug(f"start getting facts for {len(hosts)} hosts")

    # Load facts for each host
    for host in hosts:
        host_id = f"{host.hostname}.{host.site}.{host.customer}"
        facts[host_id] = load_host_facts(config=config, host=host)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished getting facts for {len(hosts)} hosts ({dur}s)")

    return facts


def load_host_facts(config: Config, host: "Host") -> Dict:
    """
    Loads datatree and returns facts for a single host.

    Args:
        config (Config): config settings.
        host (BaseHost): host instance.

    Returns:
        Dict: host facts.
    """
    # ensure kit path is in pythonpath
    if sys.path[0] != config.kit_path:
        logger.debug(f"appending kit to PYTHONPATH: {config.kit_path}")
        sys.path.insert(0, config.kit_path)

    frozen_vars = []  # Used for immutable/protected vars.
    facts = {**host.dict(include_facts=False)}  # Add host inventory facts.

    ts_start = time.perf_counter()
    logger.debug(f"{host.id}: start loading facts")

    def _load_vars(mod: ModuleType):
        """
        Function loads vars from a datatree file or directory (python module).
        """
        # Pull out dict of all variables and their types
        variables = {
            attr_name: type(attr_value)
            for attr_name, attr_value in mod.__dict__.items()
            if isinstance(attr_value, VALID_DATA_TYPES)
            and not attr_name.startswith("_")
        }

        for var, var_type in variables.items():
            # Action is defined via type hints
            var_action = getattr(
                Actions,
                getattr(mod, "__annotations__", {}).get(var, ""),
                DEFAULT_ACTION,
            )

            # Frozen variables cannot be overwritten so first value wins
            if var_action == Actions.frozen and var not in frozen_vars:
                frozen_vars.append(var)
                facts[var] = getattr(mod, var)  # set value first and only time
                continue

            # Skip frozen variables
            if var in frozen_vars:
                continue

            # List explicit merge
            if var_type == list and var_action == Actions.merge_with:
                facts[var] = getattr(mod, var) + facts.get(var, [])

            # Dict explicit merge
            elif var_type == dict and var_action == Actions.merge_with:
                facts[var] = merge_utils.merge(
                    facts.get(var, {}), getattr(mod, var), flags=MERGE_TYPE
                )
                # facts[var] = {**getattr(mod, var), **facts.get(var, {})}

            # Replace
            else:
                facts[var] = getattr(mod, var)

    for raw_path in config.datatree_lookup_paths:
        try:
            path = raw_path.format(
                **host.dict(include_facts=False)
            )  # replace path vars
        except KeyError as e:
            logger.critical(
                f"{host.id}: datatree path variable for missing {e}: {raw_path}"
            )
            sys.exit(1)

        try:
            mod = importlib.import_module(path)
            logger.debug(f"{host.id}: imported module: {path}")

        except ModuleNotFoundError:
            logger.debug(
                f"{host.id}: module not found path='{path}' raw_path='{raw_path}'"
            )
            continue

        # Load host python file or module __init__.py if host is directory
        logger.info(f"{host.id}: loading facts file='{mod.__name__}' path='{path}'")
        _load_vars(mod)

        # If host is directory then load any nested fact files
        for submod_info in pkgutil.iter_modules(getattr(mod, "__path__")):
            # Import fact file
            try:
                logger.info(
                    f"{host.id}: loading facts file='{submod_info.name}' path='{path}'"
                )
                submod = importlib.import_module(path + "." + submod_info.name)
            except (Exception, RecursionError) as e:
                logger.error(
                    f"{host.id}: error loading facts file='{submod_info.name}' path='{path}'"
                )
                logger.exception(e)
                sys.exit(1)

            _load_vars(submod)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"{host.id}: finished loading facts ({dur}s)")

    return facts


def facts_to_json_string(facts: Dict) -> str:
    """
    Returns string encoded JSON dump from facts

    Args:
        facts (Dict): facts data.

    Returns:
        str: JSON encoded string.
    """

    def _serializer(data):
        """
        Method used to help JSON encoder with unfamiliar objects.
        """
        if isinstance(data, BaseModel):
            return data.dict()
        if isinstance(data, Enum):
            return data.value
        if isinstance(data, IPv4Interface):
            return str(data)

        return str(data)

    return json.dumps(facts, indent=4, default=_serializer)
