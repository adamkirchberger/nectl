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

import pytest
import pathlib

import nectl.settings

from nectl.settings import Settings


@pytest.fixture(scope="function")
def mock_datatree(tmp_path) -> pathlib.PosixPath:
    """
    Creates a datatree mock data and returns the path.

    Returns:
        pathlib.PosixPath: path to tmp datatree.
    """
    root = tmp_path / "datatree"
    root.mkdir()
    (root / "__init__.py").write_text("")

    (root / "glob" / "common").mkdir(parents=True)
    (root / "glob" / "roles").mkdir(parents=True)

    # Make fake customers
    for customer in ["acme", "hooli"]:
        c = root / "customers" / customer
        c.mkdir(parents=True)

        (c / "common").mkdir()
        (c / "roles").mkdir()
        (c / "sites").mkdir()

        # Make fake sites
        for site in ["london", "newyork"]:
            s = c / "sites" / site
            s.mkdir(parents=True)

            (s / "common").mkdir(parents=True)
            (s / "roles").mkdir(parents=True)

            # Add deployment group
            (s / "common" / "deployment_group.py").write_text(
                f"deployment_group = 'prod_{'1' if site == 'london' else '2'}'"
            )

            hosts = s / "hosts"
            hosts.mkdir(parents=True)

            # Make fake hosts
            for hostname in ["core0", "core1"]:
                host = hosts / hostname
                host.mkdir()

                role = "primary" if hostname == "core0" else "backup"

                # Add OS details to host
                (host / "__init__.py").write_text(
                    f'role="{role}"\nos_name = "fakeos"\nos_version = "1.2.3"'
                )

    return root


@pytest.fixture(scope="function")
def mock_template_generator():
    """
    Returns function which can be used to generate templates using provided
    config object that contains kit path.

    Returns:
        Callable: template generating function.
    """

    def template_generator(settings: Settings):
        templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
        templates.mkdir()

        # Create fakeos template
        (templates / "fakeos.py").write_text(
            "def hostname_section(hostname):\n"
            "    print(f'hostname is: {hostname}')\n"
            "\n"
            "def os_section(os_name):\n"
            "    print(f'os_name is: {os_name}')\n"
            "\n"
            "def end_section():\n"
            "    print('template end')\n"
        )

    return template_generator


@pytest.fixture(scope="function")
def mock_settings(mock_datatree) -> Settings:
    """
    Creates mock settings with a datatree.

    Returns:
        settings: Settings settings.
    """
    datatree_path = mock_datatree

    settings = Settings(
        kit_path=str(datatree_path.parent),
        settings_path=str(datatree_path.parent) + "/kit.py",
        datatree_dirname="datatree",
        datatree_lookup_paths=(
            "datatree.glob.common",
            "datatree.glob.roles.{role}",
            "datatree.customers.{customer}.common",
            "datatree.customers.{customer}.roles.{role}",
            "datatree.customers.{customer}.sites.{site}.common",
            "datatree.customers.{customer}.sites.{site}.roles.{role}",
            "datatree.customers.{customer}.sites.{site}.hosts.{hostname}",
        ),
        hosts_glob_pattern="customers/*/sites/*/hosts/*",
        hosts_hostname_regex=".*/sites/.*/hosts/(.*)$",
        hosts_site_regex=".*/sites/(.*)/hosts/.*",
        hosts_customer_regex=".*/customers/(.*)/sites/.*",
    )

    # Patch config load to use mocked config
    nectl.settings.load_settings = lambda: settings

    return settings


@pytest.fixture(scope="function")
def mock_checks_generator():
    """
    Returns function which can be used to generate checks using provided
    config object that contains kit path.

    Returns:
        Callable: checks generating function.
    """

    def checks_generator(settings: Settings):
        checks = pathlib.Path(settings.kit_path) / settings.checks_dirname
        checks.mkdir()

        # Create check file using functions
        (checks / "check_one.py").write_text(
            "# match all hosts\n"
            "__hosts_filter__ = lambda host: host\n"
            "\n"
            "def check_os_version(host):\n"
            "  assert host.os_version == '1.2.3'\n"
        )

        # Create check file using functions with filter
        (checks / "check_two.py").write_text(
            "# match newyork hosts\n"
            "__hosts_filter__ = lambda host: host.site == 'newyork'\n"
            "\n"
            "def check_site(host):\n"
            "    assert host.site == 'newyork'\n"
        )

        # Create check file using classes
        (checks / "check_three.py").write_text(
            "class CheckOsVersion:\n"
            "    # match all hosts\n"
            "    \n"
            "    def check_os_version(self, host):\n"
            "        assert host.os_version == '1.2.3'\n"
        )

        # Create check file using classes with filter
        (checks / "check_four.py").write_text(
            "class CheckLondon:\n"
            "    # match london hosts\n"
            "    __hosts_filter__ = lambda host: host.site == 'london'\n"
            "    \n"
            "    def check_site(self, host):\n"
            "        assert host.site == 'london'\n"
        )

    return checks_generator
