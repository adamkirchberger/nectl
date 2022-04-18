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

# Data Models

## Summary

Data models are used to define rules and structure on how data is defined within the datatree. Using a data model you can define rules for field names, data types, required fields and default values.

Models should be kept in your network kit and be version controlled.

The convention is to name the directory `models` but this is not enforced.

Data models can be written using Pydantic, dataclasses or plain Python classes. Pydantic will provide additional features like validation out of the box, so this is recommended if validation is required for your kit.

Data models can be nested and reference other data models to create complex structures to fit your needs.

## Examples

- [Simple model](#simple-model)
- [Model with validation](#model-with-validation)
- [Model referencing another model](#model-referencing-another-model)
- [Model with nested child models](#model-with-nested-child-models)

### Simple model

A data model for a VLAN could look like this

```python
# demo-kit/models/vlan.py

from pydantic import BaseModel

class VLAN(BaseModel):
    name: str
    vlan_id: int
    description: str = ""
```

### Model with validation

A VLAN data model with validation to ensure the `vlan_id` and `name` are valid could look like this

```python
# demo-kit/models/vlan.py

from pydantic import BaseModel, Field, validator

class VLAN(BaseModel):
    name: str
    vlan_id: int = Field(..., gt=0, le=4096)
    description: str = ""

    @validator("name")
    def name_must_not_have_spaces(cls, v):
        if " " in v:
            raise ValueError("must not have spaces")
        return v
```

### Model referencing another model

A network interface data model which has fields that use the VLAN model above could look like this

```python
# demo-kit/models/interface.py

from typing import List
from pydantic import BaseModel

from models.vlan import VLAN

class Interface(BaseModel):
    name: str
    description: str = ""
    untagged_vlan: VLAN = None
    tagged_vlans: List[VLAN] = []
```

### Model with nested child models

You can also nest models if they are only relevant to the parent model for example with a BGP routing data model which defines some basic local parameters and a list of neighbour parameters.

```python
# demo-kit/models/routing.py

from typing import List
from pydantic import BaseModel
from ipaddress import IPv4Address

class BGPConfig(BaseModel):
    local_as: int
    router_id: IPv4Address

    class BGPNeighbor(BaseModel):
        remote_as: int
        address: IPv4Address

    neighbors: List[BGPNeighbor]
```
