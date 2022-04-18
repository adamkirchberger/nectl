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

from models.network import RoutedInterface

interfaces = {
    "ge-0/0/0": RoutedInterface(
        name="ge-0/0/0",
        description="facing:router1.nyc",
        ip="172.16.0.0/31",
        enabled=True,
    ),
    "ge-0/0/1": RoutedInterface(
        name="ge-0/0/1",
        description="facing:firewall1.ldn",
        ip="172.16.0.2/31",
        enabled=True,
    ),
}
