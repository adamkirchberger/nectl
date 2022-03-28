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
import sys
import pytest
from unittest.mock import patch

from nectl.exceptions import DiscoveryError
from nectl.data.hosts import Host, _get_host_datatree_path_vars


def test_should_return_str_when_creating_host_and_returning_repr(mock_settings):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN host
    host = Host(hostname="host1", site="london", _settings=settings)

    # WHEN requesting string representation
    host_str = str(host)

    # THEN expect to match
    assert host_str == (
        "Host(id='host1.london', hostname='host1', site='london', "
        "customer=None, role=None, manufacturer=None, model=None, "
        "os_name=None, os_version=None, serial_number=None, asset_tag=None, "
        "mgmt_ip=None)"
    )


@pytest.mark.parametrize(
    "host_opts,expected_id",
    (
        (
            {
                "hostname": "host1",
                "site": None,  # no site value
                "customer": None,  # no customer value
            },
            "host1",  # id should be hostname
        ),
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
    ),
)
def test_should_return_id_when_creating_host_with_opts(host_opts, expected_id):
    # GIVEN host opts
    host_opts = host_opts

    # WHEN creating host
    host = Host(**host_opts, _settings=None)

    # THEN expect id
    assert host.id == expected_id


def test_should_raise_error_when_host_mgmt_ip_is_invalid():
    # GIVEN invalid mgmt ip
    mgmt_ip = "10.0.0.999"

    with pytest.raises(DiscoveryError) as error:
        # WHEN creating host with mgmt_ip
        host = Host(hostname="host1", site="london", mgmt_ip=mgmt_ip, _settings=None)

    # THEN expect error
    assert "has invalid mgmt_ip" in str(error.value)


def test_should_return_attribute_when_accessing_attribute_not_in_class_but_present_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london", _settings=None)

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london", "location": "dc1-rack101"}

    # WHEN accessing location attribute which is not defined in Host class
    location = host.location

    # THEN expect location to match fact value
    assert location == "dc1-rack101"


def test_should_return_none_when_accessing_attribute_not_in_class_and_also_not_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london", _settings=None)

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london"}

    # WHEN accessing location attribute which is not in class or facts
    location = host.location

    # THEN expect location to be None
    assert location is None


def test_should_raise_error_when_accessing_undefined_protected_attribute_in_host_class():
    # GIVEN host
    host = Host(hostname="host1", site="london", _settings=None)

    with pytest.raises(AttributeError) as error:
        # WHEN accessing protected attribute which does not exist
        foo = host._foo

    # THEN expect error
    assert str(error.value) == "'Host' object has no attribute '_foo'"


def test_should_return_attributes_when_getting_host_attributes_using_host_file(
    tmp_path,
):
    # GIVEN tmp kit
    kit = tmp_path

    # GIVEN tmp host path
    hosts_path = kit / "datatree" / "hosts"
    hosts_path.mkdir(parents=True)

    # GIVEN host file with role
    (hosts_path / "foonode.py").write_text("role = 'foorole'\n")

    # GIVEN mock kit in path
    sys.path.insert(0, str(kit))

    # WHEN getting host attributes
    path_vars = _get_host_datatree_path_vars(
        host_path=str(hosts_path / "foonode.py"), datatree_dirname="datatree"
    )

    # THEN expect role var
    assert path_vars["role"] == "foorole"


def test_should_return_attributes_when_getting_host_attributes_using_host_directory(
    tmp_path,
):
    # GIVEN tmp kit
    kit = tmp_path

    # GIVEN tmp host path
    hosts_path = kit / "datatree" / "hosts"
    hosts_path.mkdir(parents=True)

    # GIVEN host module with init file with role
    (hosts_path / "foonode").mkdir()
    (hosts_path / "foonode" / "__init__.py").write_text("role = 'foorole'\n")

    # GIVEN mock kit in path
    sys.path.insert(0, str(kit))

    # WHEN getting host attributes
    path_vars = _get_host_datatree_path_vars(
        host_path=str(hosts_path / "foonode.py"), datatree_dirname="datatree"
    )

    # THEN expect role var
    assert path_vars["role"] == "foorole"


def test_should_return_empty_dict_when_getting_host_attributes_using_host_file(
    tmp_path,
):
    # GIVEN tmp kit
    kit = tmp_path

    # GIVEN tmp host path
    hosts_path = kit / "datatree" / "hosts"
    hosts_path.mkdir(parents=True)

    # GIVEN host file with non core variable
    (hosts_path / "foonode.py").write_text("timezone = 'utc'\n")

    # GIVEN mock kit in path
    sys.path.insert(0, str(kit))

    # WHEN getting host attributes
    path_vars = _get_host_datatree_path_vars(
        host_path=str(hosts_path / "foonode.py"), datatree_dirname="datatree"
    )

    # THEN expect blank
    assert path_vars == {}


def test_should_return_empty_dict_when_getting_host_attributes_using_host_file(
    tmp_path,
):
    # GIVEN tmp kit
    kit = tmp_path

    # GIVEN tmp host path
    hosts_path = kit / "datatree" / "hosts"
    hosts_path.mkdir(parents=True)

    # GIVEN host file with non core variable
    (hosts_path / "foonode.py").write_text("timezone = 'utc'\n")

    # GIVEN mock kit in path
    sys.path.insert(0, str(kit))

    # WHEN getting host attributes
    path_vars = _get_host_datatree_path_vars(
        host_path=str(hosts_path / "foonode.py"), datatree_dirname="datatree"
    )

    # THEN expect blank
    assert path_vars == {}


@patch("sys.exit")
def test_should_raise_error_when_getting_host_attributes_using_invalid_host(
    mock_exit,
    tmp_path,
):
    # GIVEN tmp kit
    kit = tmp_path

    # GIVEN tmp host path
    hosts_path = kit / "datatree" / "hosts"
    hosts_path.mkdir(parents=True)

    # GIVEN host file with invalid python
    (hosts_path / "foonode.py").write_text("foo =!= invalid\n")

    # GIVEN mock kit in path
    sys.path.insert(0, str(kit))

    # WHEN getting host attributes
    _get_host_datatree_path_vars(
        host_path=str(hosts_path / "foonode.py"), datatree_dirname="datatree"
    )

    # THEN expect exit to be called
    mock_exit.assert_called_with(1)
