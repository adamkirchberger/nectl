import pytest
from napalm import get_network_driver


@pytest.fixture(scope="module")
def napalm_driver(host):
    driver = get_network_driver(host.os_name)

    with driver(
        hostname=host.mgmt_ip,
        username=host.username,
        password=host.password,
        timeout=30,
        optional_args={"ssh_config_file": "~/.ssh/config"},
    ) as device:
        yield device
