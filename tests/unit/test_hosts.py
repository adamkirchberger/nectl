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

import nectl.config
from nectl.data.hosts import Host


def test_should_return_str_when_creating_host_and_returning_repr(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN host
    host = Host(hostname="host1", site="london", _config=config)

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
    host = Host(**host_opts, _config=None)

    # THEN expect id
    assert host.id == expected_id


def test_should_return_attribute_when_accessing_attribute_not_in_class_but_present_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london", _config=None)

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london", "location": "dc1-rack101"}

    # WHEN accessing location attribute which is not defined in Host class
    location = host.location

    # THEN expect location to match fact value
    assert location == "dc1-rack101"


def test_should_return_none_when_accessing_attribute_not_in_class_and_also_not_in_facts():
    # GIVEN host
    host = Host(hostname="host1", site="london", _config=None)

    # GIVEN facts are overriden
    host._facts = {"hostname": "host1", "site": "london"}

    # WHEN accessing location attribute which is not in class or facts
    location = host.location

    # THEN expect location to be None
    assert location is None


def test_should_raise_error_when_accessing_undefined_protected_attribute_in_host_class():
    # GIVEN host
    host = Host(hostname="host1", site="london", _config=None)

    with pytest.raises(AttributeError) as error:
        # WHEN accessing protected attribute which does not exist
        foo = host._foo

    # THEN expect error
    assert str(error.value) == "'Host' object has no attribute '_foo'"
