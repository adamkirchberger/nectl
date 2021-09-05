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

from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class Host:
    """
    Defines a single host which has been discovered in the datatree
    """

    # pylint: disable=R0902

    hostname: str
    site: str
    customer: str
    role: Optional[str] = ""
    manufacturer: Optional[str] = "default"
    model: Optional[str] = "default"
    os: Optional[str] = ""
    os_version: Optional[str] = ""
    serial_number: Optional[str] = ""
    asset_tag: Optional[str] = ""
    id: str = ""

    @property  # type: ignore
    def id(self) -> str:
        """
        Returns unique name for host from facts

        Example:
            hostname.site.customer
        """
        # pylint: disable=E0102
        return f"{self.hostname}.{self.site}.{self.customer}"

    @id.setter
    def id(self, v):
        """
        This field is a read only property
        """

    def dict(self) -> Dict[str, Any]:
        """
        Returns a dict with reordered fields.
        """
        return {
            "id": self.id,
            "hostname": self.hostname,
            "site": self.site,
            "customer": self.customer,
            "role": self.role,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "os": self.os,
            "os_version": self.os_version,
            "serial_number": self.serial_number,
            "asset_tag": self.asset_tag,
        }
