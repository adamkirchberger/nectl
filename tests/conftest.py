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

import nectl.config

from nectl.config import Config


@pytest.fixture(scope="function")
def mock_datatree(tmp_path) -> pathlib.PosixPath:
    """
    Creates a datatree mock data and returns the path.

    Returns:
        pathlib.PosixPath: path to tmp datatree.
    """
    root = tmp_path / "data"
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
            site = c / "sites" / site
            site.mkdir(parents=True)

            (site / "common").mkdir(parents=True)
            (site / "roles").mkdir(parents=True)

            hosts = site / "hosts"
            hosts.mkdir(parents=True)

            # Make fake hosts
            for hostname in ["core0", "core1"]:
                host = hosts / hostname
                host.mkdir()

                # Add OS details to host
                (host / "host.py").write_text(
                    'os_name = "fakeos"\nos_version = "1.2.3"'
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

    def template_generator(config: Config):
        templates = pathlib.Path(config.kit_path) / config.templates_dirname
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
def mock_config(mock_datatree) -> Config:
    """
    Creates mock config with a datatree.

    Returns:
        Config: config settings.
    """
    datatree_path = mock_datatree

    conf = Config(
        kit_path=str(datatree_path.parent),
        config_path=str(datatree_path.parent) + "/config.yaml",
        datatree_lookup_paths=(
            "data.glob.common",
            "data.glob.roles.{role}",
            "data.customers.{customer}.common",
            "data.customers.{customer}.roles.{role}",
            "data.customers.{customer}.sites.{site}.common",
            "data.customers.{customer}.sites.{site}.roles.{role}",
            "data.customers.{customer}.sites.{site}.hosts.{hostname}",
        ),
        hosts_glob_pattern="customers/*/sites/*/hosts/*",
        hosts_hostname_regex=".*/sites/.*/hosts/(.*)$",
        hosts_site_regex=".*/sites/(.*)/hosts/.*",
        hosts_customer_regex=".*/customers/(.*)/sites/.*",
    )

    # Patch config load to use mocked config
    nectl.config.load_config = lambda: conf

    return conf
