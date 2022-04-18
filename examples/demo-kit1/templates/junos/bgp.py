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

from typing import List
from models.network import BGPNeighbor


def bgp_local_as_config(local_as: int = None):
    if local_as:
        print(f"set routing-options autonomous-system {local_as}")


def bgp_neighbors_config(bgp_neighbors: List[BGPNeighbor] = None):
    if bgp_neighbors:
        print("set protocols bgp group ebgp type external")
        for neighbor in bgp_neighbors:
            print(
                f"set protocols bgp group ebgp neighbor {neighbor.ip} description {neighbor.description} peer-as {neighbor.peer_as}"
            )
