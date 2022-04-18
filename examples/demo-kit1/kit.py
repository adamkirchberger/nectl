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

datatree_lookup_paths = [
    "datatree.common",
    "datatree.roles.{role}",
    "datatree.sites.{site}.common",
    "datatree.sites.{site}.roles.{role}",
    "datatree.sites.{site}.hosts.{hostname}",
]

hosts_glob_pattern = "sites/*/hosts/*"
hosts_hostname_regex = "sites/.*/hosts/(.*)$"
hosts_site_regex = "sites/(.*)/hosts/.*"
