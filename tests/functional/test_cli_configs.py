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
from unittest.mock import patch
import click

from nectl.cli import cli_root


def test_should_return_config_when_running_cli_configs_render_command(
    cli_runner, mock_settings, mock_template_generator
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN args
    args = ["configs", "render", "-h", "core0", "-s", "london", "-c", "acme"]

    # GIVEN expected rendered config
    rendered_config = "hostname is: core0\n" "os_name is: fakeos\n" "template end\n"

    # GIVEN expected staged output directory
    staged_dir = f"{settings.kit_path}/{settings.staged_configs_dir}"

    # GIVEN template exists in kit directory
    mock_template_generator(settings)

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output to cli
    assert result.output == "1 configs created.\n"

    # THEN expect config file to be created
    with open(
        f"{staged_dir}/core0.london.acme.{settings.configs_file_extension}",
        "r",
        encoding="utf-8",
    ) as fh:
        assert fh.read() == rendered_config


@patch("nectl.configs.cli.Nectl")
def test_should_run_get_when_running_cli_configs_get_command(
    mock_nectl, cli_runner, mock_settings
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN args
    args = ["configs", "get"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect method to be called
    assert mock_nectl.return_value.get_configs.called

    # THEN expect to be successful
    assert result.exit_code == 0


@patch("nectl.configs.cli.Nectl")
def test_should_run_diff_when_running_cli_configs_diff_command(
    mock_nectl, cli_runner, mock_settings, tmp_path
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN diff method returns diff path with no files
    mock_nectl.return_value.diff_configs.return_value = tmp_path

    # GIVEN args
    args = ["configs", "diff"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect method to be called
    assert mock_nectl.return_value.diff_configs.called

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output to mention 0 diff was created
    assert "0 config diffs created." in result.output


@patch("nectl.configs.cli.Nectl")
def test_should_run_apply_when_running_cli_configs_apply_command(
    mock_nectl, cli_runner, mock_settings, tmp_path
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN diff directory with diff file
    diff_dir = tmp_path
    (diff_dir / "foonode.txt").write_text("foobar\n")

    # GIVEN apply method returns diff path
    mock_nectl.return_value.apply_configs.return_value = diff_dir

    # GIVEN args
    args = ["configs", "apply", "-y"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect method to be called
    assert mock_nectl.return_value.apply_configs.called

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output to mention 1 diff was created
    assert "1 config diffs created." in result.output
