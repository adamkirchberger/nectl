import click

from ..logging import logging_opts


@click.group(help="Verification commands.")
@logging_opts
def tests():
    """
    Tests CLI group.
    """


@tests.command(name="list")
@click.pass_context
@logging_opts
def list_cmd(ctx):
    """
    Use this command to list all configured tests.
    """
    raise NotImplementedError


@tests.command(name="run")
@click.pass_context
@logging_opts
def run_cmd(ctx):
    """
    Use this command to run tests.
    """
    raise NotImplementedError
