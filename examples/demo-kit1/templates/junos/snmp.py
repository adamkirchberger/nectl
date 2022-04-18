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


def snmp_public(snmp_public_auth, snmp_public_clients):
    # Set SNMP public community auth
    print(f"set snmp community public authorization {snmp_public_auth}")
    # Set SNMP public community allowed clients
    for client in snmp_public_clients:
        print(f"set snmp community public clients {client}")
