import pathlib

from nectl.data.hosts import Host
from nectl.data.facts_utils import load_host_facts


def test_should_return_global_ntp_servers_list_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN NTP servers has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_servers = ["global.ntp.com"]')

    # WHEN loading facts for host
    facts = load_host_facts(host=host, config=config)

    # THEN expect ntp_server in facts
    assert "ntp_servers" in facts.keys(), facts

    # THEN expect ntp_servers to be list
    assert isinstance(facts.get("ntp_servers"), list)

    # THEN expect ntp_servers value to match global servers
    assert facts.get("ntp_servers") == ["global.ntp.com"]


def test_should_return_global_roles_merged_ntp_servers_list_when_loading_facts(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host with switch role
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_servers = ["global.ntp.com"]')

    # GIVEN additional NTP server has been defined in datatree at site roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["switch.global.ntp.com"]'
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, config=config)

    # THEN expect ntp_servers in facts
    assert "ntp_servers" in facts.keys(), facts

    # THEN expect ntp_servers to be list
    assert isinstance(facts.get("ntp_servers"), list)

    # THEN expect ntp_servers value to have global and role value
    assert facts.get("ntp_servers") == ["switch.global.ntp.com", "global.ntp.com"]


def test_should_return_site_common_merged_ntp_servers_list_when_loading_facts(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP servers has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_servers = ["global.ntp.com"]')

    # GIVEN NTP servers has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["switch.global.ntp.com"]'
    )

    # GIVEN NTP servers has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["london.acme.ntp.com"]'
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, config=config)

    # THEN expect ntp_servers in facts
    assert "ntp_servers" in facts.keys(), facts

    # THEN expect ntp_servers to be list
    assert isinstance(facts.get("ntp_servers"), list)

    # THEN expect ntp_servers value to match site common server
    assert facts.get("ntp_servers") == [
        "london.acme.ntp.com",
        "switch.global.ntp.com",
        "global.ntp.com",
    ]


def test_should_return_host_only_replaced_ntp_servers_list_when_loading_facts(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP servers has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_servers = ["global.ntp.com"]')

    # GIVEN NTP servers has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["switch.global.ntp.com"]'
    )

    # GIVEN NTP servers has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["london.acme.ntp.com"]'
    )

    # GIVEN NTP server has been defined in datatree at host level with replace
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "ntp.py"
    ).write_text(
        "from nectl import actions\n"
        'ntp_server: actions.replace_with = ["core0.london.acme.ntp.com"]'
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, config=config)

    # THEN expect ntp_servers in facts
    assert "ntp_servers" in facts.keys(), facts

    # THEN expect ntp_servers to be list
    assert isinstance(facts.get("ntp_servers"), list)

    # THEN expect ntp_servers value to have host replaced value only
    assert facts.get("ntp_server") == ["core0.london.acme.ntp.com"]


def test_should_return_global_frozen_ntp_servers_list_when_loading_facts_and_also_site_frozen(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP servers has been defined in datatree globally with frozen action
    (data / "glob" / "common" / "ntp.py").write_text(
        "from nectl import actions\n" 'ntp_servers: actions.frozen = ["global.ntp.com"]'
    )

    # GIVEN NTP servers has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.merge_with = ["switch.global.ntp.com"]'
    )

    # GIVEN NTP servers has been defined in datatree at site common level with frozen action
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.frozen = ["london.acme.ntp.com"]'
    )

    # GIVEN NTP server has been defined in datatree at host level with replace
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "ntp.py"
    ).write_text(
        "from nectl import actions\n"
        'ntp_servers: actions.replace_with = ["core0.london.acme.ntp.com"]'
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, config=config)

    # THEN expect ntp_servers in facts
    assert "ntp_servers" in facts.keys(), facts

    # THEN expect ntp_servers to be list
    assert isinstance(facts.get("ntp_servers"), list)

    # THEN expect ntp_servers value to be frozen global value which is set first
    assert facts.get("ntp_servers") == ["global.ntp.com"]
