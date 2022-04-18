<!--
 Copyright (C) 2022 Adam Kirchberger

 This file is part of Nectl.

 Nectl is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 Nectl is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with Nectl.  If not, see <http://www.gnu.org/licenses/>.
-->

# External Integration

## Summary

Because Python is used at all stages, this enables you to easily create external integrations.

You might decide to have some dynamic datatree facts which fetch external data from an API or maybe send fact values to an API for validation before generating a template. The integrations are infinite and completely up to you.

## Examples

These examples should help give you an idea of the kind of integrations that are possible.

### Reading values from environment variables

In this example the value of a fact is being fetched from environment variables.

This can be useful to pull in secrets and avoid saving them in your repo.

```python
# demo-kit/datatree/common/auth.py

import os

# Global username and password
username = os.getenv("NECTL_SSH_USERNAME", default="lab-user")
password = os.getenv("NECTL_SSH_PASSWORD", default="lab-password")
```

### Creating interfaces from Netbox

In this example the interface configuration for an access switch is generated using dynamic facts from Netbox.

This can be useful to have some facts declared statically in the datatree like uplink configuration, but allow access port descriptions and VLAN ID's to come from an external source.

```python
# demo-kit/datatree/sites/ldn/switch1/interfaces.py

import os
import pynetbox

from models.network import Interface

nb = pynetbox.api(
    url=os.getenv("NETBOX_URL"),
    token=os.getenv("NETBOX_TOKEN")
)


def get_interface_from_netbox(interface_name: str) -> Interface:
    """
    Create Interface using data from Netbox.
    """
    iface = nb.dcim.interfaces.get(device="switch1", site="test1", name=interface_name)

    return Interface(
        name=interface_name,
        description=iface.description,
        untagged_vlan=iface.untagged_vlan.vid if iface.untagged_vlan else None,
        tagged_vlans=[v.vid for v in iface.tagged_vlans]
        if iface.tagged_vlans
        else None,
    )


interfaces = {
    # Access ports using Netbox data
    "ge-0/0/0": get_interface_from_netbox("ge-0/0/0"),
    "ge-0/0/1": get_interface_from_netbox("ge-0/0/1"),
    "ge-0/0/2": get_interface_from_netbox("ge-0/0/2"),
    # Uplink
    "et-0/1/0": Interface(
        name="et-0/1/0",
        description="uplink",
        untagged_vlan=999,
        tagged_vlans=[10, 20, 30],
    ),
}
```
