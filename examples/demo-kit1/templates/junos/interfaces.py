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

from typing import Dict
from models.network import RoutedInterface


def mgmt_interface(mgmt_ip, mgmt_netmask_length=24):
    print(
        f"set interfaces fxp0 unit 0 family inet address {mgmt_ip}/{mgmt_netmask_length}"
    )


def routed_interfaces(interfaces: Dict[str, RoutedInterface] = []):
    if interfaces:
        for iface in interfaces.values():
            # Only configure RoutedInterface's
            if isinstance(iface, RoutedInterface):
                # If not enabled then set disable
                if iface.enabled is False:
                    print(f"set interfaces {iface.name} disable")

                # Set description
                print(f"set interfaces {iface.name} description {iface.description}")

                # Set IP
                print(
                    f"set interfaces {iface.name} unit 0 family inet address {iface.ip}"
                )
