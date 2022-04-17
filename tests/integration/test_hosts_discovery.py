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

# pylint: disable=C0116
import pytest

from nectl.settings import Settings
from nectl.datatree.hosts import Host, get_all_hosts, get_filtered_hosts
from nectl.exceptions import DiscoveryError


def test_should_return_8_hosts_when_getting_all_hosts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # WHEN fetching all hosts
    hosts = get_all_hosts(settings=settings)

    # THEN expect each host to be of Host type
    for host in hosts:
        assert isinstance(host, Host), host

    # THEN expect to have 8 hosts
    assert len(hosts) == 8


def test_should_raise_error_when_when_getting_all_hosts_and_hostname_regex_is_invalid(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN hostname regex won't match hostname
    settings.hosts_hostname_regex = ".*/foo/(.*)$"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(settings=settings)

    # THEN expect error message
    assert "failed to extract hostname from path string" in str(error.value)


def test_should_raise_error_when_when_getting_all_hosts_and_site_regex_is_invalid(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN site regex won't match site
    settings.hosts_site_regex = ".*/foo/(.*)/hosts/.*"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(settings=settings)

    # THEN expect error message
    assert "failed to extract site from path string" in str(error.value)


def test_should_raise_error_when_when_getting_all_hosts_and_customer_regex_is_invalid(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer regex won't match customer
    settings.hosts_customer_regex = ".*/foo/(.*)/sites/.*"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(settings=settings)

    # THEN expect error message
    assert "failed to extract customer from path string" in str(error.value)


def test_should_return_no_customer_when_when_getting_all_hosts_and_no_customer_regex_is_supplied(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer regex is not set in settings
    settings.hosts_customer_regex = None

    # WHEN fetching all hosts
    hosts = get_all_hosts(settings=settings)

    # THEN expect site to be set
    assert hosts[0].site is not None

    # THEN expect customer to be none
    assert hosts[0].customer is None


def test_should_return_no_customer_and_site_when_when_getting_all_hosts_and_no_customer_or_site_regex_is_supplied(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer and site regex is not set in settings
    settings.hosts_customer_regex = None
    settings.hosts_site_regex = None

    # WHEN fetching all hosts
    hosts = get_all_hosts(settings=settings)

    # THEN expect customer to be none
    assert hosts[0].customer is None

    # THEN expect site to be none
    assert hosts[0].customer is None


def test_should_return_empty_list_when_getting_filtered_hosts_that_dont_exist(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer that doesn't exist
    customer = "foobar"

    # GIVEN site
    site = "london"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(settings=settings, site=site, customer=customer)

    # THEN expect result to be empty list
    assert hosts == []


def test_should_return_2_hosts_when_getting_filtered_hosts_by_site_and_customer(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer
    customer = "acme"

    # GIVEN site
    site = "london"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(settings=settings, site=site, customer=customer)

    # THEN expect each result to be of Host type
    for host in hosts:
        assert isinstance(host, Host), host

    # THEN expect to have 2 hosts
    assert len(hosts) == 2


def test_should_return_2_hosts_when_getting_filtered_hosts_by_site_and_role(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN role
    role = "primary"

    # GIVEN site
    site = "london"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(settings=settings, role=role, site=site)

    # THEN expect each result to be of Host type
    for host in hosts:
        assert isinstance(host, Host), host



def test_should_return_2_hosts_when_getting_filtered_hosts_by_customer_and_deployment_group(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer
    customer = "acme"

    # GIVEN deployment group
    deployment_group = "prod_1"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(
        settings=settings, customer=customer, deployment_group=deployment_group
    )

    # THEN expect to have 2 hosts
    assert len(hosts) == 2

    for host in hosts:
        # THEN expect each result to be of Host type
        assert isinstance(host, Host), host

        # THEN expect host customer
        assert host.customer == customer

        # THEN expect host deployment group
        assert host.deployment_group == deployment_group


def test_should_return_host_properties_when_getting_filtered_hosts_by_site_and_customer_and_hostname(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN customer
    customer = "acme"

    # GIVEN site
    site = "london"

    # GIVEN hostname
    hostname = "core0"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(
        settings=settings, site=site, customer=customer, hostname=hostname
    )

    # THEN expect one host
    assert len(hosts) == 1

    # THEN expect Host type
    assert isinstance(hosts[0], Host)

    # THEN expect properties to match
    assert hosts[0].customer == customer
    assert hosts[0].site == site
    assert hosts[0].hostname == hostname
    assert hosts[0].id == f"{hostname}.{site}.{customer}"


def test_should_return_hosts_when_getting_all_hosts_that_are_not_directories(tmp_path):
    # GIVEN data dir
    datatree_path = tmp_path / "test" / "datatree"
    datatree_path.mkdir(parents=True)

    settings = Settings(
        kit_path=str(datatree_path.parent),
        settings_path=str(datatree_path.parent) + "/kit.py",
        datatree_dirname="datatree",
        datatree_lookup_paths=(
            "datatree.common",
            "datatree.roles.{role}",
            "datatree.sites.{site}.common",
            "datatree.sites.{site}.roles.{role}",
            "datatree.sites.{site}.hosts.{hostname}",
        ),
        hosts_glob_pattern="sites/*/hosts/*",
        hosts_hostname_regex=".*/sites/.*/hosts/(.*)$",
        hosts_site_regex=".*/sites/(.*)/hosts/.*",
    )

    # GIVEN hosts directory
    (datatree_path / "sites" / "london" / "hosts").mkdir(parents=True)

    # GIVEN host which is defined as single file not directory
    (datatree_path / "sites" / "london" / "hosts" / "foonode.py").write_text(
        'os_name = "fakeos"'
    )

    # WHEN fetching all hosts
    hosts = get_all_hosts(settings=settings)

    # THEN expect total hosts
    assert len(hosts) == 1

    # THEN expect id
    assert hosts[0].id == "foonode.london"

    # THEN expect os
    assert hosts[0].os_name == "fakeos"
