# Copyright (C) 2022 Adam Kirchberger
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

import pytest
import logging
import click


from nectl.logging import logging_opts, setup_logging, get_logger


def test_should_return_logger_when_getting_logger():
    # WHEN calling get_logger
    logger = get_logger()

    # THEN expect to have a logger
    assert isinstance(logger, logging.Logger)


@pytest.mark.parametrize(
    "v_count,expected",
    (
        (0, logging.ERROR),
        (1, logging.INFO),
        (2, logging.DEBUG),
    ),
)
def test_should_set_correct_logging_level_based_on_supplied_verbose_flag_count(
    v_count, expected
):
    # GIVEN verbosity count
    verbosity = v_count

    # GIVEN logger
    logger = get_logger()

    # WHEN setting up logging
    setup_logging(verbosity)

    # THEN expect level to be set to expected
    assert logger.getEffectiveLevel() == expected


@pytest.mark.parametrize(
    "v_count,expected",
    (
        (0, logging.ERROR),
        (1, logging.INFO),
        (2, logging.DEBUG),
    ),
)
def test_should_return_logging_when_using_logging_dectorator_on_click_command(
    cli_runner, v_count, expected
):
    # GIVEN verbosity arg based on count
    args = ["-v"] * v_count

    # GIVEN logger
    logger = get_logger()

    # GIVEN mock command which does nothing
    @click.command()
    @logging_opts
    def mock_command():
        return

    # WHEN cli command is run with verbosity arg
    result = cli_runner.invoke(mock_command, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect log level
    assert logger.getEffectiveLevel() == expected

    # THEN if "-v" arg supplied then expect level to be in output
    if v_count > 0:
        assert f"logging level: {logging.getLevelName(expected)}" in result.output
