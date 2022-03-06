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
import pytest

from nectl.exceptions import SettingsFileError
from nectl.settings import load_settings, APP_VERSION


def test_should_raise_error_when_loading_settings_and_filepath_is_not_string():
    # GIVEN invalid path to settings
    settings_path = 12.34

    # WHEN loading settings
    with pytest.raises(TypeError) as error:
        load_settings(settings_path)

    # THEN expect error
    assert str(error.value) == "filepath must be str"


def test_should_raise_error_when_loading_settings_that_does_not_exist():
    # GIVEN path to file that does not exist
    settings_path = "kit/kit.py"

    # WHEN loading settings
    with pytest.raises(SettingsFileError) as error:
        load_settings(settings_path)

    # THEN expect error
    assert str(error.value) == "settings file not found 'kit/kit.py'"


def test_should_raise_error_when_loading_settings_file_with_invalid_extension(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN settings file which is not a valid format
    conf_file = kit_dir / "settings.xml"

    # GIVEN settings file content is XML which is not allowed
    conf_file.write_text("<settings><foo /><bar /></settings>")

    # WHEN loading settings
    with pytest.raises(SettingsFileError) as error:
        load_settings(str(conf_file))

    # THEN expect error
    assert str(error.value) == "settings file must have '.py' extension"


def test_should_raise_error_when_loading_settings_file_with_invalid_format(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN settings file which is a valid format
    conf_file = kit_dir / "kit.py"

    # GIVEN settings file content is XML which is not expected python
    conf_file.write_text("<settings><foo /><bar /></settings>")

    # WHEN loading settings
    with pytest.raises(SettingsFileError) as error:
        load_settings(str(conf_file))

    # THEN expect error
    assert "settings file is not valid: invalid syntax" in str(error.value)


def test_should_return_config_when_loading_settings_from_valid_file(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN settings file
    conf_file = kit_dir / "kit.py"

    # GIVEN settings file content
    conf_file.write_text(
        "datatree_lookup_paths=['data.a', 'data.b', 'data.c']\n"
        "hosts_glob_pattern='customers/*/sites/*/hosts/*'\n"
        "hosts_hostname_regex='.*/sites/.*/hosts/(.*)$'\n"
        "hosts_site_regex='.*/sites/(.*)/hosts/.*'\n"
        "hosts_customer_regex='.*/customers/(.*)/sites/.*'\n"
    )

    # WHEN loading settings from file
    settings = load_settings(str(conf_file))

    # THEN expect config values to match
    assert settings.datatree_lookup_paths == ["data.a", "data.b", "data.c"]
    assert settings.hosts_glob_pattern == "customers/*/sites/*/hosts/*"
    assert settings.hosts_hostname_regex == ".*/sites/.*/hosts/(.*)$"
    assert settings.hosts_site_regex == ".*/sites/(.*)/hosts/.*"
    assert settings.hosts_customer_regex == ".*/customers/(.*)/sites/.*"

    # THEN expect kit path to be set to tmp path
    assert settings.kit_path == str(kit_dir)


def test_should_fail_when_loading_settings_and_lookup_paths_is_string(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN settings file
    conf_file = kit_dir / "kit.py"

    # GIVEN settings file content
    conf_file.write_text(
        "datatree_lookup_paths='data.a, data.b, data.c'\n"
        "hosts_glob_pattern='customers/*/sites/*/hosts/*'\n"
        "hosts_hostname_regex='.*/sites/.*/hosts/(.*)$'\n"
        "hosts_site_regex='.*/sites/(.*)/hosts/.*'\n"
        "hosts_customer_regex='.*/customers/(.*)/sites/.*'\n"
    )

    # WHEN loading settings from file
    with pytest.raises(SettingsFileError) as error:
        load_settings(str(conf_file))

    # THEN expect error message
    assert "value is not a valid list" in str(error.value)


def test_should_fail_when_loading_settings_and_lookup_paths_not_defined(tmp_path):
    # GIVEN kit directory
    kit_dir = tmp_path / "kit"
    kit_dir.mkdir()

    # GIVEN settings file
    conf_file = kit_dir / "kit.py"

    # GIVEN settings file content
    conf_file.write_text(
        "hosts_glob_pattern='customers/*/sites/*/hosts/*'\n"
        "hosts_hostname_regex='.*/sites/.*/hosts/(.*)$'\n"
        "hosts_site_regex='.*/sites/(.*)/hosts/.*'\n"
        "hosts_customer_regex='.*/customers/(.*)/sites/.*'\n"
    )

    # WHEN loading settings from file
    with pytest.raises(SettingsFileError) as error:
        load_settings(str(conf_file))

    # THEN expect field required error
    assert "field required" in str(error.value)

    # THEN expect missing variable name in error
    assert "datatree_lookup_paths\n" in str(error.value)
