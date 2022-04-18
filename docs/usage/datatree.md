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

# Datatree & Facts Usage

The network control CLI tool provides the following actions for working with the datatree and facts.

?> All logs are written to `nectl.log` at the root of your network kit. To log events to the terminal use `-v`, additional `v`'s will increase the verbosity.

## List Hosts

This will display a table which lists all hosts and their core facts. This can be useful when adding or removing hosts to ensure that they are being picked up.

```bash
# Display all hosts
nectl datatree list-hosts

# Display hosts in single site
nectl datatree list-hosts --site ldn
```

## Check facts

This will run a check on the datatree and inform you of any errors.

```bash
# Check facts for all hosts
nectl datatree get-facts --check

# Check facts in single site
nectl datatree get-facts --site ldn --check

# Check facts for single host
nectl datatree get-facts --site ldn --hostname firewall1 --check
```

## Export facts

This will print out all resulting inherited host facts in a JSON format. The output can be parsed by another tool or sent to a database.

```bash
# Export all host facts
nectl datatree get-facts

# Filter export to single site
nectl datatree get-facts --site ldn

# Filter export to single host
nectl datatree get-facts --site ldn --hostname firewall1
```
