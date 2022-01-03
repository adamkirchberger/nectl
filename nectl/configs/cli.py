import sys
import click

from ..logging import logging_opts
from ..exceptions import DiscoveryError, RenderError
from ..data.hosts import get_filtered_hosts
from .render import render_hosts


@click.group(help="Configuration commands.")
@logging_opts
def configs():
    """
    Configs CLI group.
    """


@configs.command(name="list-templates", help="List available templates.")
@click.pass_context
@logging_opts
def list_templates_cmd(ctx):
    """
    Use this command to list all templates.
    """
    raise NotImplementedError


@configs.command(name="render", help="Render configs for hosts.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--directory", help="Write templates to directory.")
@click.pass_context
@logging_opts
def render_cmd(ctx, hostname: str, customer: str, site: str, role: str, directory: str):
    """
    Use this command to render configurations for hosts.
    """
    try:
    hosts = get_filtered_hosts(hostname, customer, site, role)
        _templates = render_hosts(hosts)
    except (DiscoveryError, RenderError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    for host_id, t in _templates.items():
        print(f"host: {host_id}")
        print(t)
        print("")


@configs.command(name="diff", help="Compare staged with active config.")
@click.pass_context
@logging_opts
def diff_cmd(ctx):
    """
    Use this command to compare staged and active configurations on hosts.
    """
    raise NotImplementedError


@configs.command(name="apply", help="Apply staged config to hosts.")
@click.pass_context
@logging_opts
def apply_cmd(ctx):
    """
    Use this command to apply staged configurations to hosts.
    """
    raise NotImplementedError


@configs.command(name="pull", help="Pull active config from hosts.")
@click.pass_context
@logging_opts
def pull_cmd(ctx):
    """
    Use this command to pull active configurations from hosts.
    """
    raise NotImplementedError
