import sys
import click

from ..logging import logging_opts
from ..exceptions import RenderError
from ..data.hosts import get_filtered_hosts
from .render import render_hosts


@click.group(help="template rendering commands")
@logging_opts
def templates():
    """
    Templates CLI group.
    """


@templates.command(name="list")
@click.pass_context
@logging_opts
def list_cmd(ctx):
    """
    Use this command to list all templates.
    """
    raise NotImplementedError


@templates.command(name="render", help="Generate templates for hosts using blueprints.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--directory", help="Write templates to directory.")
@click.pass_context
@logging_opts
def render_cmd(ctx, hostname: str, customer: str, site: str, role: str, directory: str):
    """
    Use this command to render templates.
    """
    hosts = get_filtered_hosts(hostname, customer, site, role)

    try:
        _templates = render_hosts(hosts)
    except RenderError as e:
        print(f"Error: {e}")
        sys.exit(1)

    for host_id, t in _templates.items():
        print(f"host: {host_id}")
        print(t)
        print("")
