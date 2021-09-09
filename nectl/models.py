from typing import Optional, Dict, Any
from dataclasses import dataclass


class BaseBlueprint:
    """
    Defines base class for a blueprint. This is only for type annotations.
    """


@dataclass
class Host:
    """
    Defines a single host which has been discovered in the datatree
    """

    # pylint: disable=R0902

    hostname: str
    site: str
    customer: str
    role: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    serial_number: Optional[str] = None
    asset_tag: Optional[str] = None
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
