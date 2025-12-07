# Copyright (C) 2023 Adam Kirchberger
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

import pathlib

from nectl.cli import cli_root


def test_should_return_checks_when_running_cli_checks_list_command(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN args
    args = ["checks", "list"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect checks to be listed
    assert (
        "<Dir checks>\n"
        "  <Module check_four.py>\n"
        "    <Class CheckLondon>\n"
        "      <Function check_site[core0.london.acme]>\n"
        "      <Function check_site[core1.london.acme]>\n"
        "      <Function check_site[core0.london.hooli]>\n"
        "      <Function check_site[core1.london.hooli]>\n"
        "  <Module check_one.py>\n"
        "    <Function check_os_version[core0.london.acme]>\n"
        "    <Function check_os_version[core1.london.acme]>\n"
        "    <Function check_os_version[core0.newyork.acme]>\n"
        "    <Function check_os_version[core1.newyork.acme]>\n"
        "    <Function check_os_version[core0.london.hooli]>\n"
        "    <Function check_os_version[core1.london.hooli]>\n"
        "    <Function check_os_version[core0.newyork.hooli]>\n"
        "    <Function check_os_version[core1.newyork.hooli]>\n"
        "  <Module check_three.py>\n"
        "    <Class CheckOsVersion>\n"
        "      <Function check_os_version[core0.london.acme]>\n"
        "      <Function check_os_version[core1.london.acme]>\n"
        "      <Function check_os_version[core0.newyork.acme]>\n"
        "      <Function check_os_version[core1.newyork.acme]>\n"
        "      <Function check_os_version[core0.london.hooli]>\n"
        "      <Function check_os_version[core1.london.hooli]>\n"
        "      <Function check_os_version[core0.newyork.hooli]>\n"
        "      <Function check_os_version[core1.newyork.hooli]>\n"
        "  <Module check_two.py>\n"
        "    <Function check_site[core0.newyork.acme]>\n"
        "    <Function check_site[core1.newyork.acme]>\n"
        "    <Function check_site[core0.newyork.hooli]>\n"
        "    <Function check_site[core1.newyork.hooli]>\n"
    ) in result.output, result.output


def test_should_return_checks_when_running_cli_checks_list_command_with_filter(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN args with london site filter
    args = ["checks", "list", "--site", "london"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect checks to be listed
    assert (
        "<Dir checks>\n"
        "  <Module check_four.py>\n"
        "    <Class CheckLondon>\n"
        "      <Function check_site[core0.london.acme]>\n"
        "      <Function check_site[core1.london.acme]>\n"
        "      <Function check_site[core0.london.hooli]>\n"
        "      <Function check_site[core1.london.hooli]>\n"
        "  <Module check_one.py>\n"
        "    <Function check_os_version[core0.london.acme]>\n"
        "    <Function check_os_version[core1.london.acme]>\n"
        "    <Function check_os_version[core0.london.hooli]>\n"
        "    <Function check_os_version[core1.london.hooli]>\n"
        "  <Module check_three.py>\n"
        "    <Class CheckOsVersion>\n"
        "      <Function check_os_version[core0.london.acme]>\n"
        "      <Function check_os_version[core1.london.acme]>\n"
        "      <Function check_os_version[core0.london.hooli]>\n"
        "      <Function check_os_version[core1.london.hooli]>\n"
    ) in result.output, result.output


def test_should_return_checks_when_running_cli_checks_list_command_with_expression(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN args with london site filter and pytest expression
    args = ["checks", "list", "--site", "london", "-k", "check_os_version"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect checks to be listed
    assert (
        "<Dir checks>\n"
        "  <Module check_one.py>\n"
        "    <Function check_os_version[core0.london.acme]>\n"
        "    <Function check_os_version[core1.london.acme]>\n"
        "    <Function check_os_version[core0.london.hooli]>\n"
        "    <Function check_os_version[core1.london.hooli]>\n"
        "  <Module check_three.py>\n"
        "    <Class CheckOsVersion>\n"
        "      <Function check_os_version[core0.london.acme]>\n"
        "      <Function check_os_version[core1.london.acme]>\n"
        "      <Function check_os_version[core0.london.hooli]>\n"
        "      <Function check_os_version[core1.london.hooli]>\n"
    ) in result.output, result.output


def test_should_return_error_when_running_cli_checks_list_command_with_invalid_checks(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN checks which will fail
    (
        pathlib.Path(settings.kit_path) / settings.checks_dirname / "check_five.py"
    ).write_text(
        "# invalid lambda\n"
        "__hosts_filter__ = lambda host.site == 'london'\n"
        "\n"
        "def check_site(self, host):\n"
        "    assert host.site == 'london'\n"
    )

    # GIVEN args
    args = ["checks", "list"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 1

    # THEN expect error message
    assert "Error: pytest encountered an error" in result.output


def test_should_return_pass_when_running_cli_checks_run_command(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN args
    args = ["checks", "run"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect pass results in output
    assert "24 passed" in result.output

    # THEN expect report path in output
    assert (
        f"report written to: {settings.kit_path}/{settings.checks_report_filename}"
    ) in result.output


def test_should_return_pass_when_running_cli_checks_run_command_with_expression(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN args with expression
    args = ["checks", "run", "-k", "check_os_version"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect pass results and deselected in output
    assert "16 passed, 8 deselected" in result.output


def test_should_return_fail_when_running_cli_checks_run_command_with_failures(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN checks which will fail
    (
        pathlib.Path(settings.kit_path) / settings.checks_dirname / "check_five.py"
    ).write_text(
        "class CheckLondon:\n"
        "    # match london hosts\n"
        "    __hosts_filter__ = lambda host: host.site == 'london'\n"
        "    \n"
        "    def check_site(self, host):\n"
        "        assert host.site == 'newyork'\n"
    )

    # GIVEN args
    args = ["checks", "run"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect exit to be 1
    assert result.exit_code == 1

    # THEN expect pass results in output
    assert "4 failed, 24 passed" in result.output


def test_should_return_error_when_running_cli_checks_run_command_with_invalid_checks(
    cli_runner, mock_settings, mock_checks_generator
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN checks exist in kit directory
    mock_checks_generator(settings)

    # GIVEN checks which will fail
    (
        pathlib.Path(settings.kit_path) / settings.checks_dirname / "check_five.py"
    ).write_text(
        "# invalid lambda\n"
        "__hosts_filter__ = lambda host.site == 'london'\n"
        "\n"
        "def check_site(self, host):\n"
        "    assert host.site == 'london'\n"
    )

    # GIVEN args
    args = ["checks", "run"]

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 1

    # THEN expect error message
    assert "Error: pytest encountered an error" in result.output
