import sys
import click

from .logging import logging_opts
from .exceptions import ConfigFileError
from .config import APP_VERSION, APP_DESCRIPTION, load_config
from .data.cli import data
from .configs.cli import configs
from .templates.cli import templates
from .tests.cli import tests


def main():
    """
    Main entrypoint
    """
    return cli_root()  # pylint: disable=E1120


@click.group(help=APP_DESCRIPTION)
@click.version_option(APP_VERSION)
@click.pass_context
@logging_opts
def cli_root(ctx):
    """
    Root CLI group
    """
    # Load config file
    try:
        config = load_config()
    except ConfigFileError as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Set context for child commands
    ctx.obj = {"config": config}


# Add child groups
cli_root.add_command(data)
cli_root.add_command(configs)
cli_root.add_command(templates)
cli_root.add_command(tests)
