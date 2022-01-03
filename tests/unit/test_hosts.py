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


def test_should_return_str_when_creating_host_and_returning_repr(mock_config):
    # GIVEN get_config() is patched to return mock_config
    nectl.config.__config = mock_config

    # GIVEN host
    host = Host(hostname="host1", site="london")

    # WHEN requesting string representation
    host_str = str(host)

    # THEN expect to match
    assert host_str == (
        "Host(id='host1.london', hostname='host1', site='london', "
        "customer=None, role=None, manufacturer=None, model=None, "
        "os_name=None, os_version=None, serial_number=None, asset_tag=None)"
    )


@pytest.mark.parametrize(
    "host_opts,expected_id",
    [
        (
            {
                "hostname": "host1",
                "site": "london",
                "customer": None,  # no customer value
            },
            "host1.london",  # id should be hostname.site
        ),
        (
            {
                "hostname": "host1",
                "site": "london",
                "customer": "acme",  # customer value
            },
            "host1.london.acme",  # id should be hostname.site.customer
        ),
    ],
)
def test_should_return_id_when_creating_host_with_opts(host_opts, expected_id):
    # GIVEN host opts
    host_opts = host_opts

    # WHEN creating host
    host = Host(**host_opts)

    # THEN expect id
    assert host.id == expected_id


def test_should_return_attribute_when_accessing_attribute_not_in_class_but_present_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london")

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london", "location": "dc1-rack101"}

    # WHEN accessing location attribute which is not defined in Host class
    location = host.location

    # THEN expect location to match fact value
    assert location == "dc1-rack101"


def test_should_return_none_when_accessing_attribute_not_in_class_and_also_not_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london")

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london"}

    # WHEN accessing location attribute which is not in class or facts
    location = host.location

    # THEN expect location to be None
    assert location is None


def test_should_raise_error_when_accessing_undefined_protected_attribute_in_host_class():
    # GIVEN host
    host = Host(hostname="host1", site="london")

    with pytest.raises(AttributeError) as error:
        # WHEN accessing protected attribute which does not exist
        foo = host._foo

    # THEN expect error
    assert str(error.value) == "'Host' object has no attribute '_foo'"
