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

# Hosts

## Summary

A host represents a single network element within your network kit. They can be physical, virtual and from any network vendor.

Hosts do not need to be reachable to be used in the datatree, unless you intend to make nectl interact with the hosts. This can be useful for testing or creating configurations for hosts that you do not have direct access to.

## Host Facts

Hosts are defined in the datatree and have the following core facts.

!> The only required variable for a host is the `hostname` which is taken from the filename.</br> Eg. `datatree/sites/ldn/hosts/{hostname}.py`

| **Name**         | **Required** | **Description**                          |
| ---------------- | ------------ | ---------------------------------------- |
| hostname         | Yes          | Host name                                |
| manufacturer     | Optional     | Manufacturer name                        |
| model            | Optional     | Model name                               |
| serial_number    | Optional     | Serial number                            |
| asset_tag        | Optional     | Asset tag                                |
| os_name          | Optional     | Operating system name                    |
| os_version       | Optional     | Operating system version                 |
| mgmt_ip          | Optional     | Management IP address                    |
| username         | Optional     | Host specific username                   |
| password         | Optional     | Host specific password                   |
| role             | Optional     | Role which can be used in datatree       |
| deployment_group | Optional     | Grouping used for staggered deployments. |

The facts above are all optional, however failure to define some of them will limit the functionality for that host. For example if a host does not have an `os_name` then a suitable driver cannot not be determined in order to control the host.

## Examples

### Single host file

This example shows a host definition.

?> Note that the hostname will be taken from the filename.

```python
# demo-kit/datatree/sites/ldn/hosts/firewall1.py

manufacturer = "juniper"
model = "srx300
serial_number = "AA2609AA0027"
asset_tag = "AABBCCDD"
os_name = "junos"
os_version = "19.4"
mgmt_ip = "192.168.0.100/24"
role = "firewalls"

# Other host facts are added to this file too
location = "rack101:ru40"
syslog_server = "10.0.0.1"
```

### Multiple host fact files

?> Hosts behave just like other facts defined in the datatree, these can be single Python files or directories (with an `__init__.py`) it makes sense to have multiple files.

The above example split up into several files could look like

```python
# demo-kit/datatree/sites/ldn/hosts/firewall1/__init__.py

# core facts
manufacturer = "juniper"
model = "srx300
serial_number = "AA2609AA0027"
asset_tag = "AABBCCDD"
os_name = "junos"
os_version = "19.4"
mgmt_ip = "192.168.0.100/24"
role = "firewalls"
```

```python
# demo-kit/datatree/sites/ldn/hosts/firewall1/location.py

# location facts
location = "rack101:ru40"
```

```python
# demo-kit/datatree/sites/ldn/hosts/firewall1/syslog.py

# syslog facts
syslog_server = "10.0.0.1"
```
