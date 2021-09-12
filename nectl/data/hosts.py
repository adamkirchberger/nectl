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
from typing import Optional, Union, Any, List, Dict
from glob import glob
from dataclasses import dataclass

from ..logging import logger
from ..config import Config, get_config
from .facts_utils import load_host_facts

HOSTS_IGNORE_REGEX = (r".*\/__pycache__.*",)


@dataclass
class Host:
    """
    Defines a host instance which has facts and templates.
    """

    hostname: str
    site: str
    customer: str
    role: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    os_name: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag: Optional[str] = None
    _facts: Union[Dict, None] = None

    @property
    def id(self) -> str:
        """
        Returns unique name for host.
        """
        return f"{self.hostname}.{self.site}.{self.customer}"

    @property
    def facts(self) -> Dict:
        """
        Returns read only facts.
        """
        if self._facts is None:
            self._facts = load_host_facts(host=self)
        return self._facts

    def __getattr__(self, name):
        """
        Handles access to attributes that are not explicitly defined. If an
        attribute exists in host facts then the value will be returned.
        """
        if not name.startswith("_") and name in self.facts:
            logger.debug(f"{self.id}: fetching undefined fact '{name}'")
            return self.facts[name]

        return object.__getattribute__(self, name)

    def __getattribute__(self, name):
        """
        Intercept calls to attributes and return the value from host facts.
        """
        ignored_attrs = ("role", "_facts")
        if object.__getattribute__(self, name) is None and name not in ignored_attrs:
            logger.debug(f"{self.id}: fetching fact '{name}'")
            return object.__getattribute__(self, "facts").get(name)

        return object.__getattribute__(self, name)

    def dict(self, include_facts=True) -> Dict[str, Any]:
        """
        Returns a dict with reordered fields.
        """
        return {
            "id": self.id,
            "hostname": self.hostname,
            "site": self.site,
            "customer": self.customer,
            "role": self.role,
            "manufacturer": self.manufacturer if include_facts else None,
            "model": self.model if include_facts else None,
            "os_name": self.os if include_facts else None,
            "os_version": self.os_version if include_facts else None,
            "serial_number": self.serial_number if include_facts else None,
            "asset_tag": self.asset_tag if include_facts else None,
        }

    def __repr__(self) -> str:
        return (
            "Host("
            + ", ".join([f"{k}={repr(v)}" for k, v in self.dict().items()])
            + ")"
        )


def get_filtered_hosts(
    hostname: str = None,
    customer: str = None,
    site: str = None,
    role: str = None,
    config: Config = get_config(),
) -> List[Host]:
    """
    Returns a list of filtered hosts

    Args:
        hostname (str): filter by hostname.
        site (str): filter by site.
        customer (str): filter by customer.
        role (str): filter by role.
        config (Config): config settings.

    Returns:
        List[Host]: list of discovered hosts.
    """
    hosts = get_all_hosts(config)

    # Filter by customer
    if customer:
        hosts = [h for h in hosts if h.customer == customer]
        logger.info(f"filtered by customer=='{customer}'")
        logger.debug(f"remaining hosts: {len(hosts)}")

    # Filter by site
    if site:
        hosts = [h for h in hosts if h.site == site]
        logger.info(f"filtered by site=='{site}'")
        logger.debug(f"remaining hosts: {len(hosts)}")

    # Filter by role
    if role:
        hosts = [h for h in hosts if h.role == role]
        logger.info(f"filtered by role == '{role}'")
        logger.debug(f"remaining hosts: {len(hosts)}")

    # Filter by hostname
    if hostname:
        hosts = [h for h in hosts if h.hostname == hostname]
        logger.info(f"filtered by hostname=='{hostname}'")
        logger.debug(f"remaining hosts: {len(hosts)}")

    if len(hosts) == 0:
        print("No hosts found.", file=sys.stderr)

    return hosts


def get_all_hosts(config: Config) -> List[Host]:
    """
    Returns list of all discovered hosts from datatree.

    Args:
        config (Config): config settings.

    Returns:
        List[Host]: list of discovered hosts.
    """
    hosts = []

    ts_start = time.perf_counter()

    path = f"{config.datatree_path}/{config.hosts_glob_pattern}"
    logger.debug(f"starting hosts discovery in: {path}")

    host_dirs = [
        h for h in glob(path) if not any(re.match(p, h) for p in HOSTS_IGNORE_REGEX)
    ]
    for host_dir in host_dirs:
        # Extract hostname
        m = re.match(config.hosts_hostname_regex, host_dir)
        if m:
            hostname = re.sub(".py$", "", m.group(1))
        else:
            logger.fatal(f"failed to extract hostname for host: {host_dir}")
            continue

        # Extract site
        m = re.match(config.hosts_site_regex, host_dir)
        if m:
            site = m.group(1)
        else:
            logger.fatal(f"failed to extract site for host: {host_dir}")
            continue

        # Extract customer
        m = re.match(config.hosts_customer_regex, host_dir)
        if m:
            customer = m.group(1)
        else:
            logger.fatal(f"failed to extract customer for host: {host_dir}")
            continue

        new_host = Host(hostname=hostname, site=site, customer=customer)
        logger.debug(f"found host '{new_host.id}' in directory: {host_dir}")
        hosts.append(new_host)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished discovery of {len(hosts)} hosts ({dur}s)")

    return hosts
