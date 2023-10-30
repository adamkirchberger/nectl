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

import re
import sys
import time
import importlib
from typing import Optional, Union, Any, List, Dict
from glob import glob
from dataclasses import dataclass, field
from ipaddress import AddressValueError, IPv4Address

from ..logging import get_logger
from ..exceptions import DiscoveryError
from ..settings import Settings, get_settings
from .facts_utils import load_host_facts

HOSTS_IGNORE_REGEX = (r".*\/__pycache__.*",)
logger = get_logger()


@dataclass
class Host:
    """
    Defines a host instance which has facts.
    """

    hostname: str
    site: Optional[str] = None
    customer: Optional[str] = None
    role: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag: Optional[str] = None
    mgmt_ip: Optional[str] = None
    deployment_group: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    _facts: Union[Dict, None] = None
    _settings: Settings = field(default_factory=get_settings)

    def __post_init__(self):
        """
        Host post transforms.
        """
        try:
            # Validate MGMT IP address
            if self.mgmt_ip:
                self.mgmt_ip = str(IPv4Address(self.mgmt_ip))
        except AddressValueError as e:
            raise DiscoveryError(f"host '{self.id}' has invalid mgmt_ip: {e}") from e

    @property
    def id(self) -> str:
        """
        Returns unique name for host.

        Example:
            hostname.site.customer
        """
        return ".".join(
            [
                attr
                for attr in [self.hostname, self.site, self.customer]
                if attr is not None
            ]
        )

    @property
    def facts(self) -> Dict:
        """
        Returns read only facts.
        """
        if self._facts is None:
            self._facts = load_host_facts(host=self, settings=self._settings)
        return self._facts

    def __getattr__(self, name):
        """
        Handles access to attributes that are not explicitly defined. If an
        attribute exists in host facts then the value will be returned.
        """
        if not name.startswith("_") and name in self.facts:
            logger.debug(f"[{self.id}] fetching fact '{name}'")
            return self.facts[name]

        if not name.startswith("_") and name not in self.facts:
            logger.warning(f"[{self.id}] fact not found '{name}'")
            return None

        raise AttributeError(f"'Host' object has no attribute '{name}'")

    def __getattribute__(self, name):
        """
        Intercept calls to attributes and return the value from host facts.
        """
        ignored_attrs = (
            "site",
            "customer",
            "role",
            "mgmt_ip",
            "_facts",
            "_settings",
        )  # don't try find value in facts
        if object.__getattribute__(self, name) is None and name not in ignored_attrs:
            logger.debug(f"[{self.id}] fetching fact '{name}'")
            return object.__getattribute__(self, "facts").get(name)

        return object.__getattribute__(self, name)

    def dict(self, include_facts=True) -> Dict[str, Any]:
        """
        Returns a dict with reordered fields.

        Args:
            include_facts (bool): If False only core facts are returned.
        """
        return {
            # Core facts from host file
            "id": self.id,
            "hostname": self.hostname,
            "site": self.site,
            "customer": self.customer,
            "role": self.role,
            # Facts from anywhere in datatree
            "deployment_group": self.deployment_group if include_facts else None,
            "manufacturer": self.manufacturer if include_facts else None,
            "model": self.model if include_facts else None,
            "os_name": self.os_name if include_facts else None,
            "os_version": self.os_version if include_facts else None,
            "serial_number": self.serial_number if include_facts else None,
            "asset_tag": self.asset_tag if include_facts else None,
            "mgmt_ip": self.mgmt_ip,
        }

    def __repr__(self) -> str:
        return (
            "Host("
            + ", ".join([f"{k}={repr(v)}" for k, v in self.dict().items()])
            + ")"
        )


def get_filtered_hosts(
    settings: Settings,
    hostname: str = None,
    customer: str = None,
    site: str = None,
    role: str = None,
    deployment_group: str = None,
) -> Dict[str, Host]:
    """
    Returns a list of filtered hosts

    Args:
        settings (Settings): config settings.
        hostname (str): filter by hostname.
        site (str): filter by site.
        customer (str): filter by customer.
        role (str): filter by role.
        deployment_group (str): filter by deployment group.

    Returns:
        Dict[str, Host]: discovered host instances mapped by host ID.

    Raises:
        DiscoveryError: if hosts cannot be successfully discovered.
    """
    filters = dict(
        customer=customer,
        site=site,
        role=role,
        deployment_group=deployment_group,
        hostname=hostname,
    )

    # Return all hosts if no filter values provided
    if all(filter is None for filter in filters.values()):
        return get_all_hosts(settings=settings)

    def is_match(host: Host) -> bool:
        """
        Returns True if host matches all filters that are not None.
        """
        for filter_name, filter_value in filters.items():
            if filter_value is not None:
                if not bool(getattr(host, filter_name) == filter_value):
                    return False
        return True

    hosts = {}

    # Loop hosts
    for host in get_all_hosts(settings=settings).values():
        # Check for match against filters
        if is_match(host):
            # Add host
            hosts[host.id] = host

    logger.info(
        f"filter matched {len(hosts)} hosts: "
        f"{','.join([host for host in hosts.keys()])}"
    )

    if len(hosts) == 0:
        print("No hosts found.", file=sys.stderr)

    return hosts


def _get_host_datatree_path_vars(host_path: str, datatree_dirname: str) -> dict:
    """
    Imports the host to retrieve core vars like 'role' which are used in
    the datatree lookup paths. These must be in host's python file or the
    __init__.py file if host is defined as a directory.

    Args:
        host_path (str): the file path to the host module.
        datatree_dirname (str): name of datatree directory.

    Returns:
        dict: host attributes used to instantiate a Host instance.
    """
    # Attributes we are interested in
    attrs = [
        "mgmt_ip",
        "role",
        "model",
        "manufacturer",
        "os_name",
        "os_version",
        "serial_number",
        "asset_tag",
    ]

    # Extract host module import path
    m = re.match(re.compile(rf".*({datatree_dirname}\/.*?)(\.py)?$"), host_path)
    if m:
        try:
            # Import host module
            mod = importlib.import_module(m.group(1).replace("/", "."))

            # Extract and return any attributes we're interested in
            return {
                attr: mod.__dict__.get(attr) for attr in attrs if mod.__dict__.get(attr)
            }
        except Exception as e:
            logger.error(f"error loading host in: {host_path}")
            logger.exception(e)
            sys.exit(1)

    return {}


def get_all_hosts(settings: Settings) -> Dict[str, Host]:
    """
    Returns list of all discovered hosts from datatree.

    Args:
        settings (Settings): config settings.

    Returns:
        Dict[str, Host]: discovered host instances mapped by host ID.

    Raises:
        DiscoveryError: if hosts cannot be successfully discovered.
    """
    hosts: Dict[str, Host] = {}
    hostname: str = ""
    site: Optional[str] = None
    customer: Optional[str] = None

    ts_start = time.perf_counter()

    path = f"{settings.datatree_path}/{settings.hosts_glob_pattern}"
    logger.debug(f"starting hosts discovery in: {path}")

    # Ensure kit path is in pythonpath
    if sys.path[0] != settings.kit_path:
        logger.debug(f"appending kit to PYTHONPATH: {settings.kit_path}")
        sys.path.insert(0, settings.kit_path)

    host_dirs = [
        h for h in glob(path) if not any(re.match(p, h) for p in HOSTS_IGNORE_REGEX)
    ]
    for host_dir in host_dirs:
        # Extract hostname
        m = re.search(re.compile(settings.hosts_hostname_regex), host_dir)
        if m:
            hostname = re.sub(".py$", "", m.group(1))
        else:
            msg = (
                f"failed to extract hostname from path string '{host_dir}' "
                f"using regex: '{settings.hosts_hostname_regex}'"
            )
            logger.critical(msg)
            raise DiscoveryError(msg)

        # Extract site for multi-site data trees
        if settings.hosts_site_regex:
            m = re.search(re.compile(settings.hosts_site_regex), host_dir)
            if m:
                site = m.group(1)
            else:
                msg = (
                    f"failed to extract site from path string '{host_dir}' "
                    f"using regex: '{settings.hosts_site_regex}'"
                )
                logger.critical(msg)
                raise DiscoveryError(msg)
        # No site single site tree
        else:
            site = None

        # Extract customer for multi-tenant data trees
        if settings.hosts_customer_regex:
            m = re.search(re.compile(settings.hosts_customer_regex), host_dir)
            if m:
                customer = m.group(1)
            else:
                msg = (
                    f"failed to extract customer from path string '{host_dir}' "
                    f"using regex: '{settings.hosts_customer_regex}'"
                )
                logger.critical(msg)
                raise DiscoveryError(msg)
        # No customer single tenant tree
        else:
            customer = None

        # Get any core host vars which are defined and use to instantiate
        host_vars = _get_host_datatree_path_vars(
            host_path=host_dir, datatree_dirname=settings.datatree_dirname
        )

        # Create host
        new_host = Host(
            hostname=hostname,
            site=site,
            customer=customer,
            _settings=settings,
            **host_vars,
        )
        logger.debug(f"found host '{new_host.id}' in: {host_dir}")
        hosts[new_host.id] = new_host

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished discovery of {len(hosts)} hosts ({dur}s)")

    return hosts
