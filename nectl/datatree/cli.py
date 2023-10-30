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
import json
import click
from tabulate import tabulate

from .. import Nectl
from ..logging import logging_opts
from ..exceptions import DiscoveryError
from .facts_utils import facts_to_json_string


@click.group(help="Inventory and datatree commands.")
@logging_opts
def datatree():
    """
    Datatree CLI group.
    """


@datatree.command(name="list-hosts", help="List hosts discovered in datatree.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.option(
    "-o",
    "--output",
    help="Output format.",
    type=click.Choice(["text", "json"]),
    default="text",
)
@click.pass_context
@logging_opts
def list_hosts_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
    output: str,
):
    """
    Use this command to list hosts discovered in the datatree.
    """
    try:
        hosts = Nectl(settings=ctx.obj["settings"]).get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
    except DiscoveryError as e:
        print(f"Error: {e}")
        sys.exit(1)

    if output == "json":
        print(
            json.dumps({h.id: h.dict() for h in hosts.values()}, indent=4, default=str)
        )
    else:
        print(
            tabulate(
                [h.dict() for h in hosts.values()],
                headers="keys",
                tablefmt="psql",
            )
        )


@datatree.command(name="get-facts", help="Get facts from datatree.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.option("--check", help="Check only with no JSON output.", is_flag=True)
@click.pass_context
@logging_opts
def get_facts_cmd(
    ctx,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
    check: bool = False,
):
    """
    Use this command to get facts for hosts defined in the datatree.
    """
    try:
        hosts = Nectl(settings=ctx.obj["settings"]).get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
    except DiscoveryError as e:
        print(f"Error: {e}")
        sys.exit(1)

    host_facts = {host.id: host.facts for host in hosts.values()}

    if not check:
        print(facts_to_json_string(host_facts))
