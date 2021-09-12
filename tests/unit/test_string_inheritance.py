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

# pylint: disable=C0116

import pathlib

from nectl.data.hosts import Host
from nectl.data.facts_utils import load_host_facts


def test_should_return_global_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server = "global.ntp.com"')

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match global server
    assert facts.get("ntp_server") == "global.ntp.com"


def test_should_return_global_roles_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host with switch role
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match global role server
    assert facts.get("ntp_server") == "switch.global.ntp.com"


def test_should_return_customer_common_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server_2 = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer common level
    (data / "customers" / "acme" / "common" / "ntp.py").write_text(
        'ntp_server = "acme.ntp.com"'
    )

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match customer common server
    assert facts.get("ntp_server") == "acme.ntp.com"


def test_should_return_customer_roles_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server_2 = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer common level
    (data / "customers" / "acme" / "common" / "ntp.py").write_text(
        'ntp_server = "acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer roles level
    (data / "customers" / "acme" / "roles" / "switch").mkdir()
    (data / "customers" / "acme" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.acme.ntp.com"'
    )

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match customer roles server
    assert facts.get("ntp_server") == "switch.acme.ntp.com"


def test_should_return_site_common_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server_2 = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer common level
    (data / "customers" / "acme" / "common" / "ntp.py").write_text(
        'ntp_server = "acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer roles level
    (data / "customers" / "acme" / "roles" / "switch").mkdir()
    (data / "customers" / "acme" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        'ntp_server = "london.acme.ntp.com"'
    )

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match site common server
    assert facts.get("ntp_server") == "london.acme.ntp.com"


def test_should_return_site_roles_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server_2 = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer common level
    (data / "customers" / "acme" / "common" / "ntp.py").write_text(
        'ntp_server = "acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer roles level
    (data / "customers" / "acme" / "roles" / "switch").mkdir()
    (data / "customers" / "acme" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        'ntp_server = "london.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site roles level
    (data / "customers" / "acme" / "sites" / "london" / "roles" / "switch").mkdir()
    (
        data / "customers" / "acme" / "sites" / "london" / "roles" / "switch" / "ntp.py"
    ).write_text('ntp_server = "switch.london.acme.ntp.com"')

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match site roles server
    assert facts.get("ntp_server") == "switch.london.acme.ntp.com"


def test_should_return_host_local_ntp_value_when_loading_facts(mock_config):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text('ntp_server_2 = "global.ntp.com"')

    # GIVEN NTP server has been defined in datatree at global roles level
    (data / "glob" / "roles" / "switch").mkdir()
    (data / "glob" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer common level
    (data / "customers" / "acme" / "common" / "ntp.py").write_text(
        'ntp_server = "acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at customer roles level
    (data / "customers" / "acme" / "roles" / "switch").mkdir()
    (data / "customers" / "acme" / "roles" / "switch" / "ntp.py").write_text(
        'ntp_server = "switch.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        'ntp_server = "london.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site roles level
    (data / "customers" / "acme" / "sites" / "london" / "roles" / "switch").mkdir()
    (
        data / "customers" / "acme" / "sites" / "london" / "roles" / "switch" / "ntp.py"
    ).write_text('ntp_server = "switch.london.acme.ntp.com"')

    # GIVEN NTP server has been defined in datatree at host level
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "ntp.py"
    ).write_text('ntp_server = "core0.london.acme.ntp.com"')

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match host level server
    assert facts.get("ntp_server") == "core0.london.acme.ntp.com"


def test_should_return_global_ntp_value_when_loading_facts_and_var_action_is_frozen(
    mock_config,
):
    # GIVEN config using mock kit
    config = mock_config

    # GIVEN datatree path
    data = pathlib.Path(config.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme", role="switch")

    # GIVEN NTP server has been defined in datatree globally
    (data / "glob" / "common" / "ntp.py").write_text(
        'from nectl import actions\nntp_server: actions.frozen = "global.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at site common level
    (data / "customers" / "acme" / "sites" / "london" / "common" / "ntp.py").write_text(
        'ntp_server = "london.acme.ntp.com"'
    )

    # GIVEN NTP server has been defined in datatree at host level
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "ntp.py"
    ).write_text('ntp_server = "core0.london.acme.ntp.com"')

    # WHEN loading facts for host
    facts = load_host_facts(config, host=host)

    # THEN expect ntp_server in facts
    assert "ntp_server" in facts.keys(), facts

    # THEN expect ntp_server value to match frozen global server
    assert facts.get("ntp_server") == "global.ntp.com"
