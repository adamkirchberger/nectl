# pylint: disable=C0116
import pytest

import nectl.config
from nectl.data.hosts import Host, get_all_hosts, get_filtered_hosts
from nectl.exceptions import DiscoveryError


def test_should_return_8_hosts_when_getting_all_hosts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # WHEN fetching all hosts
    hosts = get_all_hosts(config=config)

    # THEN expect each host to be of Host type
    for host in hosts:
        assert isinstance(host, Host), host

    # THEN expect to have 8 hosts
    assert len(hosts) == 8


def test_should_raise_error_when_when_getting_all_hosts_and_hostname_regex_is_invalid(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN hostname regex won't match hostname
    config.hosts_hostname_regex = ".*/foo/(.*)$"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(config=config)

    # THEN expect error message
    assert "failed to extract hostname from path string" in str(error.value)


def test_should_raise_error_when_when_getting_all_hosts_and_site_regex_is_invalid(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN site regex won't match site
    config.hosts_site_regex = ".*/foo/(.*)/hosts/.*"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(config=config)

    # THEN expect error message
    assert "failed to extract site from path string" in str(error.value)


def test_should_raise_error_when_when_getting_all_hosts_and_customer_regex_is_invalid(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN customer regex won't match customer
    config.hosts_customer_regex = ".*/foo/(.*)/sites/.*"

    with pytest.raises(DiscoveryError) as error:
        # WHEN fetching all hosts
        get_all_hosts(config=config)

    # THEN expect error message
    assert "failed to extract customer from path string" in str(error.value)


def test_should_return_no_customer_when_when_getting_all_hosts_and_no_customer_regex_is_supplied(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN customer regex is not set in config
    config.hosts_customer_regex = None

    # WHEN fetching all hosts
    hosts = get_all_hosts(config=config)

    # THEN expect customer to be none
    assert hosts[0].customer is None


def test_should_return_empty_list_when_getting_filtered_hosts_that_dont_exist(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN customer that doesn't exist
    customer = "foobar"

    # GIVEN site
    site = "london"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(config=config, site=site, customer=customer)

    # THEN expect result to be empty list
    assert hosts == []


def test_should_return_2_hosts_when_getting_filtered_hosts_by_site_and_customer(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN customer
    customer = "acme"

    # GIVEN site
    site = "london"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(config=config, site=site, customer=customer)

    # THEN expect each result to be of Host type
    for host in hosts:
        assert isinstance(host, Host), host

    # THEN expect to have 2 hosts
    assert len(hosts) == 2


def test_should_return_host_properties_when_getting_filtered_hosts_by_site_and_customer_and_hostname(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN customer
    customer = "acme"

    # GIVEN site
    site = "london"

    # GIVEN hostname
    hostname = "core0"

    # WHEN fetching hosts and using filters
    hosts = get_filtered_hosts(
        config=config, site=site, customer=customer, hostname=hostname
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
