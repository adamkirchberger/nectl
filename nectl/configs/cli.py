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

import os
import sys
import click

from .. import Nectl
from ..logging import logging_opts, get_logger
from ..exceptions import (
    DiscoveryError,
    RenderError,
    DriverError,
)

logger = get_logger()


@click.group(help="Configuration commands.")
@logging_opts
def configs():
    """
    Configs CLI group.
    """


@configs.command(name="render", help="Render configs for hosts.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.pass_context
@logging_opts
def render_cmd(
    ctx, hostname: str, customer: str, site: str, role: str, deployment_group: str
):
    """
    Use this command to render configurations for hosts.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
        nectl.render_configs(hosts=hosts.values())
    except (DiscoveryError, RenderError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{len(hosts)} configs created.")


@configs.command(name="diff", help="Compare active configs to rendered configs.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.option("-u", "--username", help="Host driver username.")
@click.option("-p", "--password", help="Host driver password.")
@click.option("-i", "--ssh-key", help="Host driver SSH private key file.")
@click.pass_context
@logging_opts
def diff_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
    username: str,
    password: str,
    ssh_key: str,
):
    """
    Use this command to compare staged and active configurations on hosts.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
        diff_dir = nectl.diff_configs(
            hosts=hosts.values(),
            username=username,
            password=password,
            ssh_private_key_file=ssh_key,
        )
    except (DiscoveryError, DriverError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{len(next(os.walk(diff_dir))[2])} config diffs created.")


@configs.command(name="apply", help="Apply staged config onto host.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.option("-u", "--username", help="Host driver username.")
@click.option("-p", "--password", help="Host driver password.")
@click.option("-i", "--ssh-key", help="Host driver SSH private key file.")
@click.option(
    "-y",
    "--assumeyes",
    help="Automatically answer yes for all questions.",
    is_flag=True,
)
@click.pass_context
@logging_opts
def apply_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
    username: str,
    password: str,
    ssh_key: str,
    assumeyes: bool = False,
):
    """
    Use this command to apply staged configurations onto hosts.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )

        print("Applying config to:")
        print("\n".join([f"- {host}" for host in hosts.keys()]))

        if not assumeyes:
            click.confirm(
                f"\nAre you sure you want to modify {len(hosts)} live hosts?",
                abort=True,
            )

        diff_dir = nectl.apply_configs(
            hosts=hosts.values(),
            username=username,
            password=password,
            ssh_private_key_file=ssh_key,
        )
    except (DiscoveryError, DriverError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{len(next(os.walk(diff_dir))[2])} config diffs created.")


@configs.command(name="get", help="Get active config from hosts.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.option("-u", "--username", help="Host driver username.")
@click.option("-p", "--password", help="Host driver password.")
@click.option("-i", "--ssh-key", help="Host driver SSH private key file.")
@click.pass_context
@logging_opts
def get_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
    username: str,
    password: str,
    ssh_key: str,
):
    """
    Use this command to get active configurations from hosts.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
        nectl.get_configs(
            hosts=hosts.values(),
            username=username,
            password=password,
            ssh_private_key_file=ssh_key,
        )
    except (DiscoveryError, DriverError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"{len(hosts)} config backups created.")
