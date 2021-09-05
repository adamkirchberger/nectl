# pylint: disable=C0116

from nectl.models import Host
from nectl.data.hosts import get_all_hosts, get_filtered_hosts


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
    hosts = get_filtered_hosts(config, site=site, customer=customer)

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
    hosts = get_filtered_hosts(config, site=site, customer=customer, hostname=hostname)

    # THEN expect one host
    assert len(hosts) == 1

    # THEN expect Host type
    assert isinstance(hosts[0], Host)

    # THEN expect properties to match
    assert hosts[0].customer == customer
    assert hosts[0].site == site
    assert hosts[0].hostname == hostname
    assert hosts[0].id == f"{hostname}.{site}.{customer}"
