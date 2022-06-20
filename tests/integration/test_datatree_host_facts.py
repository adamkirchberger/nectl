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

import pathlib

from nectl.datatree.hosts import Host
from nectl.datatree.facts_utils import load_host_facts


def test_should_return_str_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with str fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text("custom_str = 'foobar'\n")

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_str" in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_str"), str)

    # THEN expect custom fact value
    assert facts.get("custom_str") == "foobar"


def test_should_return_int_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with int fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text("custom_int = 999\n")

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_int" in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_int"), int)

    # THEN expect custom fact value
    assert facts.get("custom_int") == 999


def test_should_return_float_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with float fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text("custom_float = 1.5\n")

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_float" in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_float"), float)

    # THEN expect custom fact value
    assert facts.get("custom_float") == 1.5


def test_should_return_list_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with list fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text("custom_list = ['foo','bar']\n")

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_list" in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_list"), list)

    # THEN expect custom fact value
    assert facts.get("custom_list") == ["foo", "bar"]


def test_should_return_dict_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with dict fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text("custom_dict = {'foo':'bar'}\n")

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_dict" in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_dict"), dict)

    # THEN expect custom fact value
    assert facts.get("custom_dict") == {"foo": "bar"}


def test_should_return_dataclass_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with dataclass fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text(
        "from dataclasses import dataclass\n"
        "\n"
        "@dataclass\n"
        "class CustomType:\n"
        "    name: str\n"
        "    enabled: bool\n"
        "\n"
        "custom_type = CustomType(name='foobar',enabled=True)\n"
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_type" in facts.keys(), facts

    # THEN expect custom type class not to be in facts
    assert "CustomType" not in facts.keys(), facts

    # THEN expect custom fact type
    assert type(facts.get("custom_type")).__name__ == "CustomType"

    # THEN expect custom fact value
    assert vars(facts.get("custom_type")) == {"name": "foobar", "enabled": True}


def test_should_return_basemodel_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with basemodel fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text(
        "from pydantic import BaseModel\n"
        "\n"
        "class CustomType(BaseModel):\n"
        "    name: str\n"
        "    enabled: bool\n"
        "\n"
        "custom_type = CustomType(name='foobar',enabled=True)\n"
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_type" in facts.keys(), facts

    # THEN expect custom type class not to be in facts
    assert "CustomType" not in facts.keys(), facts

    # THEN expect custom fact type
    assert type(facts.get("custom_type")).__name__ == "CustomType"

    # THEN expect custom fact value
    assert vars(facts.get("custom_type")) == {"name": "foobar", "enabled": True}


def test_should_return_pydantic_dataclass_fact_from_host_when_loading_facts(
    mock_settings,
):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with pydantic dataclass fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text(
        "from pydantic.dataclasses import dataclass\n"
        "\n"
        "@dataclass\n"
        "class CustomType:\n"
        "    name: str\n"
        "    enabled: bool\n"
        "\n"
        "custom_type = CustomType(name='foobar',enabled=True)\n"
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_type" in facts.keys(), facts

    # THEN expect custom type class not to be in facts
    assert "CustomType" not in facts.keys(), facts

    # THEN expect custom fact type
    assert type(facts.get("custom_type")).__name__ == "CustomType"

    # THEN expect custom fact value
    assert vars(facts.get("custom_type")) == {
        "name": "foobar",
        "enabled": True,
        "__initialised__": True,
    }


def test_should_return_dataclass_list_fact_from_host_when_loading_facts(mock_settings):
    # GIVEN settings using mock kit
    settings = mock_settings

    # GIVEN datatree path
    data = pathlib.Path(settings.datatree_path)

    # GIVEN host
    host = Host(hostname="core0", site="london", customer="acme")

    # GIVEN host has been defined with dataclass list fact
    (
        data / "customers" / "acme" / "sites" / "london" / "hosts" / "core0" / "info.py"
    ).write_text(
        "from dataclasses import dataclass\n"
        "\n"
        "@dataclass\n"
        "class CustomType:\n"
        "    name: str\n"
        "    enabled: bool\n"
        "\n"
        "custom_type = [\n"
        "    CustomType(name='foo',enabled=True),\n"
        "    CustomType(name='bar',enabled=False),\n"
        "]\n"
    )

    # WHEN loading facts for host
    facts = load_host_facts(host=host, settings=settings)

    # THEN expect custom fact to be in facts
    assert "custom_type" in facts.keys(), facts

    # THEN expect custom type class not to be in facts
    assert "CustomType" not in facts.keys(), facts

    # THEN expect custom fact type
    assert isinstance(facts.get("custom_type"), list)

    # THEN expect inner element type
    assert type(facts.get("custom_type")[0]).__name__ == "CustomType"

    # THEN expect custom fact values
    assert vars(facts.get("custom_type")[0]) == {"name": "foo", "enabled": True}
    assert vars(facts.get("custom_type")[1]) == {"name": "bar", "enabled": False}
