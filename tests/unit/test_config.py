# pylint: disable=C0116

import re
import pytest

from nectl.exceptions import ConfigFileError
from nectl.config import load_config


def test_should_return_config_when_loading_config_from_json_file(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN config file
    conf_file = kit_dir / "config.json"

    # GIVEN config file content is JSON
    conf_file.write_text(
        "{"
        '"datatree_lookup_paths": ["data.a", "data.b", "data.c"],'
        '"hosts_glob_pattern": "customers/*/sites/*/hosts/*",'
        '"hosts_hostname_regex": ".*/sites/.*/hosts/(.*)$",'
        '"hosts_site_regex": ".*/sites/(.*)/hosts/.*",'
        '"hosts_customer_regex": ".*/customers/(.*)/sites/.*"'
        "}"
    )

    # WHEN loading config from file
    config = load_config(str(conf_file))

    # THEN expect config values to match
    assert config.datatree_lookup_paths == ["data.a", "data.b", "data.c"]
    assert config.hosts_glob_pattern == "customers/*/sites/*/hosts/*"
    assert config.hosts_hostname_regex == ".*/sites/.*/hosts/(.*)$"
    assert config.hosts_site_regex == ".*/sites/(.*)/hosts/.*"
    assert config.hosts_customer_regex == ".*/customers/(.*)/sites/.*"

    # THEN expect kit path to be set to tmp path
    assert config.kit_path == str(kit_dir)


def test_should_return_config_when_loading_config_from_yaml_file(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN config file
    conf_file = kit_dir / "config.yaml"

    # GIVEN config file content is YAML
    conf_file.write_text(
        "---\n"
        "datatree_lookup_paths: [data.a, data.b, data.c]\n"
        "hosts_glob_pattern: customers/*/sites/*/hosts/*\n"
        "hosts_hostname_regex: .*/sites/.*/hosts/(.*)$\n"
        "hosts_site_regex: .*/sites/(.*)/hosts/.*\n"
        "hosts_customer_regex: .*/customers/(.*)/sites/.*\n"
    )

    # WHEN loading config from file
    config = load_config(str(conf_file))

    # THEN expect config values to match
    assert config.datatree_lookup_paths == ["data.a", "data.b", "data.c"]
    assert config.hosts_glob_pattern == "customers/*/sites/*/hosts/*"
    assert config.hosts_hostname_regex == ".*/sites/.*/hosts/(.*)$"
    assert config.hosts_site_regex == ".*/sites/(.*)/hosts/.*"
    assert config.hosts_customer_regex == ".*/customers/(.*)/sites/.*"

    # THEN expect kit path to be set to tmp path
    assert config.kit_path == str(kit_dir)


def test_should_fail_when_loading_config_and_lookup_paths_not_string(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN config file
    conf_file = kit_dir / "config.yaml"

    # GIVEN config file content is YAML
    conf_file.write_text(
        "---\n"
        "datatree_lookup_paths: data.a, data.b, data.c\n"
        "hosts_glob_pattern: customers/*/sites/*/hosts/*\n"
        "hosts_hostname_regex: .*/sites/.*/hosts/(.*)$\n"
        "hosts_site_regex: .*/sites/(.*)/hosts/.*\n"
        "hosts_customer_regex: .*/customers/(.*)/sites/.*\n"
    )

    # WHEN loading config from file
    with pytest.raises(ConfigFileError) as error:
        load_config(str(conf_file))

    # THEN expect error message
    assert "value is not a valid list" in str(error.value)


def test_should_fail_when_loading_config_and_lookup_paths_not_defined(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN config file
    conf_file = kit_dir / "config.yaml"

    # GIVEN config file content is YAML
    conf_file.write_text(
        "---\n"
        "hosts_glob_pattern: customers/*/sites/*/hosts/*\n"
        "hosts_hostname_regex: .*/sites/.*/hosts/(.*)$\n"
        "hosts_site_regex: .*/sites/(.*)/hosts/.*\n"
        "hosts_customer_regex: .*/customers/(.*)/sites/.*\n"
    )

    # WHEN loading config from file
    with pytest.raises(ConfigFileError) as error:
        load_config(str(conf_file))

    # THEN expect field required error
    assert "field required" in str(error.value)

    # THEN expect missing variable name in error
    assert "datatree_lookup_paths\n" in str(error.value)


def test_should_return_config_when_loading_config_with_blueprints_map(
    tmp_path,
):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN config file
    conf_file = kit_dir / "config.yaml"

    # GIVEN config file content is YAML
    conf_file.write_text(
        "---\n"
        "datatree_lookup_paths: [data.a, data.b, data.c]\n"
        "hosts_glob_pattern: customers/*/sites/*/hosts/*\n"
        "hosts_hostname_regex: .*/sites/.*/hosts/(.*)$\n"
        "hosts_site_regex: .*/sites/(.*)/hosts/.*\n"
        "hosts_customer_regex: .*/customers/(.*)/sites/.*\n"
        "blueprints_map:\n"
        "  fakeos:FakeOs:\n"
        "    os_regex: 'fakeos'\n"
        "    os_version_regex: '5.*'\n"
    )

    # WHEN loading config from file
    config = load_config(str(conf_file))

    # THEN expect blueprint to exist in map
    assert "fakeos:FakeOs" in config.blueprints_map

    # THEN expect values to be regex patterns
    assert config.blueprints_map["fakeos:FakeOs"].os_regex == re.compile("fakeos")
    assert config.blueprints_map["fakeos:FakeOs"].os_version_regex == re.compile("5.*")
