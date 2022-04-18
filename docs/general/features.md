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

# Features

These are some of the features may be of interest

- [Data modelling and validation](#data-modelling-and-validation)
- [Data facts and inheritance](#data-facts-and-inheritance)
- [Encrypted facts](#encrypted-facts)
- [Config rendering using templates](#config-rendering-using-templates)
- [Host config manipulation using drivers](#host-config-manipulation-using-drivers)
- [Integration with external API's and databases](#integration-with-external-api39s-and-databases)
- [Isolated environments with unique requirements](#isolated-environments-with-unique-requirements)
- **Python used for all the above.**

---

## Data modelling and validation

- Data modelling is supported using Python classes with type hints.
- Simple validation is built-in by using class constructors to enforce required arguments.
- Additional validation can be implemented easily using tools like Pydantic.

See guide on [Data Models](guide/data-models.md)

## Data facts and inheritance

- Data facts are defined as variable declarations in python files.
- Files are arranged in a hierarchical tree using a user-defined structure.
- Fact inheritance can be defined at root, leaf or any intermediate level.
- Facts can be declared as constants or replaceable.
- Deep merging of lists and dicts is supported.

See guide on [Datatree](guide/datatree.md)

## Encrypted Facts

- Data facts can be encrypted using any Python encryption library, eg: rsa.
- Keys can be passed via env var or local files.

## Config rendering using templates

- Templates are used to define how configurations should be built.
- Templates are network OS specific and can include many sections.

See guide on [Templates](guide/templates.md)

## Host config manipulation using drivers

- Drivers are used to communicate with live hosts and perform config actions.
- Nectl includes some network vendor drivers and supports custom drivers too.

See guide on [Drivers](guide/drivers.md)

## Integration with external API's and databases

- Facts used in datatree files can be callable functions.
- Functions to pull from API\s or databases can be implemented and invoked during fact gathering.
- Template files can include functions to pull external data, eg: allow lists.

See guide on [External Integration](guide/external-integration.md)

## Isolated environments with unique requirements

- Kits are used to provide fully isolated environments.
- Kits are version controlled and can be used to control access and permissions.
- Kits are self-sufficient and contain all dependent resources for an environment.

See guide on [Kits](guide/kits.md)
