import sys
import logging
import functools
from typing import Callable, TypeVar
import coloredlogs  # type: ignore
import click


T = TypeVar("T")


def get_logger() -> logging.Logger:
    """
    Returns app logger.

    Returns:
        logging.Logger: logger.
    """
    return logging.getLogger("nectl")


def logging_opts(func: Callable[..., T]) -> Callable[..., T]:
    """
    Click command logging options decorator.
    """
    logger = get_logger()

    @click.option("-v", help="Increase logging (-vv, -vvv for more).", count=True)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Configure logging
        setup_logging(kwargs.get("v"))
        del kwargs["v"]  # remove verbosity argument for child commands

        # Debug show input arguments
        logger.debug(f"input args='{args}' kwargs='{kwargs}'")

        # Debug show loaded config
        try:
            logger.debug(f'config: {args[0].obj.get("config")}')
        except IndexError:
            pass
        except AttributeError:
            pass

        return func(*args, **kwargs)

    return wrapper


def setup_logging(v: int = 0):
    """
    Setup logging level based on verbosity flags.

    Args:
        v (int): verbosity level.
    """
    logging_levels = {
        0: logging.CRITICAL,
        1: logging.ERROR,
        2: logging.INFO,
        3: logging.DEBUG,
    }
    _level = logging_levels[min(v, len(logging_levels) - 1)]
    coloredlogs.install(_level, logger=get_logger())
    if v > 0:
        print(f"logging level: {logging.getLevelName(_level)}", file=sys.stderr)
