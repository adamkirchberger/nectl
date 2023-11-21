# Copyright (C) 2023 Adam Kirchberger
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


from typing import List
import pytest

from ..logging import get_logger
from ..datatree.hosts import Host


FILTER_VARIABLE_NAME = "__hosts_filter__"


logger = get_logger()


class ChecksPlugin:
    """
    Nectl pytest checks plugin.

    Example:

    __hosts_filter__ = lambda host: host.site == "nyc"

    def check_site(host):
        assert host.site == "nyc"

    """

    def __init__(self, hosts: List[Host]) -> None:
        """
        A Pytest plugin that generates additional tests for each matching host.

        Args:
            hosts (List[Host]): list of hosts to check.
        """
        self._hosts = hosts
        self.passed = 0
        self.failed = 0
        self.tests = []
        self.tests_selected = []
        self.tests_deselected = []

    @pytest.fixture(scope="module")
    def _nectl_host(self, request):
        return request.param

    @pytest.fixture(scope="module")
    def host(self, _nectl_host):
        return _nectl_host

    def pytest_runtest_logreport(self, report):
        """
        Update counters.
        """
        if report.when != "call":
            return
        if report.passed:
            self.passed += 1
        elif report.failed:
            self.failed += 1

    def pytest_collection_modifyitems(self, session):
        """
        Intercept tests and add them to a tests list.
        """
        self.tests = self.tests_selected = [item.nodeid for item in session.items]

    def pytest_deselected(self, items):
        """
        Handle select/deselect of tests.
        """
        self.tests_deselected = [item.nodeid for item in items]
        self.tests_selected = [
            item for item in self.tests if item not in self.tests_deselected
        ]

    def pytest_generate_tests(self, metafunc):
        """
        Dynamically parametrize checks based on matching datatree hosts.
        """
        if "_nectl_host" in metafunc.fixturenames:
            # Pull hosts filter from classes
            if hasattr(metafunc.cls, FILTER_VARIABLE_NAME):
                hosts_filter = getattr(metafunc.cls, FILTER_VARIABLE_NAME)
            # Pull hosts filter from module
            elif hasattr(metafunc.module, FILTER_VARIABLE_NAME):
                hosts_filter = getattr(metafunc.module, FILTER_VARIABLE_NAME)
            else:
                hosts_filter = lambda host: host  # default return all hosts

            # Filter hosts
            hosts = [host for host in self._hosts if hosts_filter(host)]

            # Skip test if there are no hosts matched
            if not hosts:
                pytest.skip("skipping as no hosts matched the test filter")

            # Repeat tests using parametrize and passing matching host instances
            metafunc.parametrize(
                "_nectl_host",
                hosts,
                ids=[host.id for host in hosts],
                scope="module",
                indirect=True,
            )
