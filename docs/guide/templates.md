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

# Templates

## Summary

Templates are used to describe how facts found in the datatree can be used to produce host specific configurations in a format that can be interpreted by the end host.

A template file is made up of several sections, each section is a standard Python function with one or more `print()` function calls. Templates are operating system specific and matched by using the template filename and the value of the host `os_name` fact.

Templates should be kept in your network kit and be version controlled.

The function name be will be your section name and function parameters should indicate facts from the datatree that the section needs, these can also specify default values.

!> If a template section needs a fact which has no default value and also cannot be found in the datatree then an error will be raised.

## Examples

### Standard template

This is an example template for an operating system called `junos`.

```python
# demo-kit/templates/junos.py

def system_hostname_config(hostname):
    print(f"set system host-name {hostname}")


def configure_ntp_servers(ntp_servers=["10.0.0.1"]):
    for server in ntp_servers:
        print(f"set ntp server {server}")
```

The template has two sections a hostname section and an NTP servers section, these can be named whatever you like.

The _system_hostname_config_ section has an argument `hostname` which is required.

The _configure_ntp_servers_ section has an argument `ntp_servers` which if not found in the datatree will use a default value of `["10.0.0.1"]`

A template can be a single file or a directory (with an `__init__.py`) which contains a collection of files, this can be useful when building large templates or managing operating system version specific templates.

### Template with sub-templates

This is a more advanced example which includes some conditional templates.

```python
# demo-kit/templates/junos/__init__.py

from nectl import get_render_facts

# Base sections applicable to all junos hosts
from .base import *

# MX specific sections
if get_render_facts().get("model").startswith("mx"):
    from .mx_sections import *

# SRX specific sections
elif get_render_facts().get("model").startswith("srx"):
    from .srx_sections import *
```

```python
# demo-kit/templates/junos/mx_sections.py

... MX sections here
```

```python
# demo-kit/templates/junos/srx_sections.py

... SRX sections here
```
