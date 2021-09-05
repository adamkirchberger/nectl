import click

from ..logging import logging_opts


@click.group(help="device configuration commands")
@logging_opts
def configs():
    """
    Configs CLI group.
    """


@configs.command()
@click.pass_context
@logging_opts
def replace(ctx):
    """
    Use this command to replace config on remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def apply(ctx):
    """
    Use this command to apply config on a remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def diff(ctx):
    """
    Use this command to compare the intended vs actual config on remote devices.
    """
    raise NotImplementedError


@configs.command()
@click.pass_context
@logging_opts
def backup(ctx):
    """
    Use this command to make a local config backup from remote devices.
    """
    raise NotImplementedError
