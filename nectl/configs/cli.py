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

import sys
import click

from ..logging import logging_opts, get_logger
from ..exceptions import (
    DiscoveryError,
    RenderError,
)
from ..data.hosts import get_filtered_hosts
from .render import render_hosts
from .utils import write_configs_to_dir
from .drivers import run_driver_method_on_hosts

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
@click.pass_context
@logging_opts
def render_cmd(ctx, hostname: str, customer: str, site: str, role: str):
    """
    Use this command to render configurations for hosts.
    """
    settings = ctx.obj["settings"]

    try:
        hosts = get_filtered_hosts(
            settings=settings,
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
        )
        renders = render_hosts(settings=settings, hosts=hosts)
    except (DiscoveryError, RenderError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    output_dir = f"{settings.kit_path}/{settings.staged_configs_dir}"

    write_configs_to_dir(configs=renders, output_dir=output_dir)

    print(f"{len(renders)} configs created.")


@configs.command(name="diff", help="Compare active configs to rendered configs.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.pass_context
@logging_opts
def diff_cmd(ctx, hostname: str, customer: str, site: str, role: str):
    """
    Use this command to compare staged and active configurations on hosts.
    """
    settings = ctx.obj["settings"]

    try:
        hosts = get_filtered_hosts(
            settings=settings,
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
        )
    except (DiscoveryError, RenderError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    sys.exit(
        run_driver_method_on_hosts(
            settings=settings,
            hosts=hosts,
            method_name="compare_config",
            description="comparing host configurations",
        )
    )


@configs.command(name="apply", help="Apply staged config onto host.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-u", "--username", help="Host driver username.")
@click.option("-p", "--password", help="Host driver password.")
@click.pass_context
@logging_opts
def apply_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    username: str,
    password: str,
):
    """
    Use this command to apply staged configurations onto hosts.
    """
    settings = ctx.obj["settings"]

    try:
        hosts = get_filtered_hosts(
            settings=settings,
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
        )
    except (DiscoveryError, RenderError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    click.confirm(
        f"Are you sure you want to modify {len(hosts)} live hosts?", abort=True
    )

    sys.exit(
        run_driver_method_on_hosts(
            settings=settings,
            hosts=hosts,
            method_name="apply_config",
            description="applying host configurations",
            username=username,
            password=password,
        )
    )


@configs.command(name="pull", help="Pull active config from hosts.")
@click.pass_context
@logging_opts
def pull_cmd(ctx):
    """
    Use this command to pull active configurations from hosts.
    """
    raise NotImplementedError
