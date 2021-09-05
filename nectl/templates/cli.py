import click

from ..logging import logging_opts


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


@templates.command(name="render")
@click.pass_context
@logging_opts
def render_cmd(ctx):
    """
    Use this command to render templates.
    """
    raise NotImplementedError
