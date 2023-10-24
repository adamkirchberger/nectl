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
from dataclasses import is_dataclass
from enum import Enum
from ipaddress import IPv4Interface
from pydantic import BaseModel  # pylint: disable=E0611
from dpath import merge, MergeType

from ..logging import get_logger
from ..settings import Settings
from .actions import Actions

if TYPE_CHECKING:
    from .hosts import Host

VALID_DATA_TYPES = (list, dict, str, int, float)
MERGE_TYPE = MergeType.ADDITIVE
logger = get_logger()


def get_facts_for_hosts(
    settings: Settings,
    hosts: List["Host"],
) -> Dict[str, Dict]:
    """
    Returns a dict of facts loaded from datatree for each provided host.

    Args:
        settings (Settings): config settings.
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
        facts[host_id] = load_host_facts(settings=settings, host=host)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished getting facts for {len(hosts)} hosts ({dur}s)")

    return facts


def load_host_facts(settings: Settings, host: "Host") -> Dict:
    """
    Loads datatree and returns facts for a single host.

    Args:
        settings (Settings): config settings.
        host (BaseHost): host instance.

    Returns:
        Dict: host facts.
    """
    # ensure kit path is in pythonpath
    if sys.path[0] != settings.kit_path:
        logger.debug(f"appending kit to PYTHONPATH: {settings.kit_path}")
        sys.path.insert(0, settings.kit_path)

    frozen_vars = []  # Used for immutable/protected vars.
    facts = {**host.dict(include_facts=False)}  # Add host inventory facts.

    ts_start = time.perf_counter()
    logger.debug(f"[{host.id}] start loading facts")

    def _load_vars(mod: ModuleType):
        """
        Function loads vars from a datatree file or directory (python module).
        """
        # Pull out dict of all variables and their types
        variables = {
            attr_name: type(attr_value)
            for attr_name, attr_value in mod.__dict__.items()
            if (
                isinstance(attr_value, VALID_DATA_TYPES)
                or is_dataclass(attr_value)
                or isinstance(attr_value, BaseModel)
            )
            and not isinstance(attr_value, type)
            and not attr_name.startswith("_")
        }

        for var, var_type in variables.items():
            # Action is defined via type hints
            var_action = getattr(
                Actions,
                getattr(mod, "__annotations__", {}).get(var, ""),
                settings.default_action,
            )

            # Frozen variables cannot be overwritten so first value wins
            if var_action == Actions.frozen and var not in frozen_vars:
                frozen_vars.append(var)
                facts[var] = getattr(mod, var)  # set value first and only time
                continue

            # Skip frozen variables
            if var in frozen_vars:
                logger.warning(
                    f"[{host.id}] attempted to modify frozen fact '{var}' from file: {mod.__file__}"
                )
                continue

            # List explicit merge
            if var_type == list and var_action == Actions.merge_with:
                facts[var] = getattr(mod, var) + facts.get(var, [])

            # Dict explicit merge
            elif var_type == dict and var_action == Actions.merge_with:
                facts[var] = merge(
                    facts.get(var, {}), getattr(mod, var), flags=MERGE_TYPE
                )

            # Replace
            else:
                facts[var] = getattr(mod, var)

    for raw_path in settings.datatree_lookup_paths:
        try:
            path = raw_path.format(
                **host.dict(include_facts=False)
            )  # replace path vars
        except KeyError as e:
            logger.critical(
                f"[{host.id}] datatree path variable missing {e}: {raw_path}"
            )
            sys.exit(1)

        try:
            # Import module
            mod = importlib.import_module(path)

            # Check if directory
            if getattr(mod, "__name__") == getattr(mod, "__package__"):
                logger.debug(f"[{host.id}] imported directory module: {path}")
            else:
                logger.debug(f"[{host.id}] imported file module: {path}")

            # Load python file or module __init__.py if is directory
            logger.debug(f"[{host.id}] loading facts file: {path}")
            _load_vars(mod)

        except ModuleNotFoundError:
            logger.debug(
                f"[{host.id}] module not found path='{path}' raw_path='{raw_path}'"
            )
            continue

        except Exception as e:
            logger.error(f"[{host.id}] error loading facts file: {path}")
            logger.exception(e)
            sys.exit(1)

        # If module is a package (directory)
        if getattr(mod, "__name__") == getattr(mod, "__package__"):
            # Then load any nested fact files
            for submod_info in pkgutil.iter_modules(getattr(mod, "__path__")):
                try:
                    logger.debug(
                        f"[{host.id}] loading facts file: {path}.{submod_info.name}"
                    )
                    submod = importlib.import_module(path + "." + submod_info.name)
                    _load_vars(submod)
                except (Exception, RecursionError) as e:
                    logger.error(
                        f"[{host.id}] error loading facts file: {path}.{submod_info.name}"
                    )
                    logger.exception(e)
                    sys.exit(1)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"[{host.id}] finished loading facts ({dur}s)")

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
        if is_dataclass(data):
            return vars(data)

        return str(data)

    return json.dumps(facts, indent=4, default=_serializer)
