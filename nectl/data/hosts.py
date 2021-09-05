import re
import sys
import time
from typing import List
from glob import glob

from ..logging import logger
from ..models import Host
from ..config import Config

HOSTS_IGNORE_REGEX = (r".*\/__pycache__.*",)


def get_filtered_hosts(
    config: Config,
    hostname: str = None,
    customer: str = None,
    site: str = None,
    role: str = None,
) -> List[Host]:
    """
    Returns a list of filtered hosts

    Args:
        config (Config): config settings.
        hostname (str): filter by hostname.
        site (str): filter by site.
        customer (str): filter by customer.
        role (str): filter by role.

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
        logger.debug(f"found {new_host} in directory: {host_dir}")
        hosts.append(new_host)

    dur = f"{time.perf_counter()-ts_start:0.4f}"
    logger.info(f"finished discovery of {len(hosts)} hosts ({dur}s)")

    return hosts
