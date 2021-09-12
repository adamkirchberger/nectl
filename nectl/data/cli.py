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

import json
import click
from tabulate import tabulate

from ..logging import logging_opts
from .hosts import get_filtered_hosts
from .facts_utils import facts_to_json_string


@click.group(help="Inventory and datatree commands")
@logging_opts
def data():
    """
    Data CLI group.
    """


@data.command(name="list-hosts", help="List hosts discovered in datatree.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
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
    ctx, hostname: str, customer: str, site: str, role: str, output: str
):
    """
    Use this command to list hosts discovered in the datatree.
    """
    hosts = get_filtered_hosts(hostname, customer, site, role)

    if output == "json":
        print(json.dumps({"hosts": [h.dict() for h in hosts]}, indent=4, default=str))
    else:
        print(
            tabulate(
                [h.dict() for h in hosts],
                headers="keys",
                tablefmt="psql",
            )
        )


@data.command(name="get-facts", help="Get facts from datatree.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.pass_context
@logging_opts
def get_facts_cmd(ctx, hostname: str, customer: str, site: str, role: str):
    """
    Use this command to get facts for hosts defined in the datatree.
    """
    hosts = get_filtered_hosts(hostname, customer, site, role)

    host_facts = {host.id: host.facts for host in hosts}

    print(facts_to_json_string(host_facts))
