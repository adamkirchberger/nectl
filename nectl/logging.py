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
import logging
import logging.config
import platform
import functools
from typing import Callable, TypeVar
import click

from .settings import get_settings
from .exceptions import SettingsFileError


T = TypeVar("T")

CONSOLE_LOGGING_LEVEL = logging.WARNING
FILE_LOGGING_LEVEL = logging.DEBUG
try:
    FILE_LOGGING_FILENAME = get_settings().kit_path + "/nectl.log"
except SettingsFileError:
    FILE_LOGGING_FILENAME = "nectl.log"
LOGGING_FORMAT = (
    f"%(asctime)s {platform.node()} %(name)s[%(process)d] %(levelname)s %(message)s"
)
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "loggers": {
        "": {
            "level": "WARNING",
            "handlers": ["file"],
        },
        "nectl": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
    "formatters": {
        "console_fmt": {
            "()": "coloredlogs.ColoredFormatter",
            "format": LOGGING_FORMAT,
            "datefmt": "%H:%M:%S",
        },
        "file_fmt": {
            "format": LOGGING_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": CONSOLE_LOGGING_LEVEL,
            "class": "logging.StreamHandler",
            "formatter": "console_fmt",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": FILE_LOGGING_LEVEL,
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "file_fmt",
            "filename": FILE_LOGGING_FILENAME,
            # "maxBytes": 500000,
            # "backupCount": 5,
        },
    },
}
logging.config.dictConfig(LOGGING_CONFIG)


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
    def wrapper(*args, v: int, **kwargs):
        # Configure logging
        setup_logging(v)

        # Debug show input arguments
        logger.debug(f"func '{func.__name__}' input args='{args}' kwargs='{kwargs}'")

        # Debug show loaded settings
        try:
            logger.debug(f'settings: {args[0].obj.get("settings")}')
        except (AttributeError, IndexError):
            pass

        return func(*args, **kwargs)

    return wrapper


def setup_logging(v: int = 0) -> None:
    """
    Setup logging level based on verbosity flags.

    Args:
        v (int): verbosity level.
    """
    # Nectl logger verbosity flag count levels
    nectl_log_levels = {
        0: logging.WARNING,
        1: logging.INFO,
        2: logging.DEBUG,
    }
    nectl_log_level = nectl_log_levels[min(v, len(nectl_log_levels) - 1)]

    # Set nectl logger console level, file log level is not changed.
    logging.getLogger("nectl").handlers[0].setLevel(nectl_log_level)

    # All loggers verbosity flag count levels
    all_log_levels = {
        0: logging.ERROR,
        1: logging.ERROR,
        2: logging.INFO,
        3: logging.DEBUG,
    }
    all_log_level = all_log_levels[min(v, len(all_log_levels) - 1)]

    # Set all loggers level
    logging.getLogger("").setLevel(all_log_level)

    if v > 0:
        print(
            (
                "logging levels:"
                f" '*'={logging.getLevelName(all_log_level)}"
                f" 'nectl'={logging.getLevelName(nectl_log_level)}"
            ),
            file=sys.stderr,
        )
