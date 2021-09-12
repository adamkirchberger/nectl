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
    hosts = get_filtered_hosts(ctx.obj.get("config"), hostname, customer, site, role)

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
    config = ctx.obj.get("config")
    hosts = get_filtered_hosts(config, hostname, customer, site, role)

    host_facts = {host.id: host.facts for host in hosts}

    print(facts_to_json_string(host_facts))
