<!--
 Copyright (C) 2025 Adam Kirchberger

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

# Checks

## Summary

Checks are used to run automated validation checks on hosts and their facts. They are implemented using a pytest plugin.

?> Note that unit tests for any utilities or datatree objects should be defined using the standard `tests`⁠ directory instead of using ⁠`checks`⁠, checks are aimed at host specific tests as a test will have multiple instances executed for each matching host.

## Configuring checks

Checks should be configured in the `checks`⁠ directory, each python file must be prepended with⁠ `check_` to be discovered and executed.

Checks will run for all hosts discovered in the datatree by default unless a filter is defined in the check.

## Running Checks

The network control CLI tool provides actions for interacting with checks.

### List Checks

```bash
# List all checks
nectl checks list
```

### Run Checks

```bash
# List all checks
nectl checks run
```

?> Use `--help` with the commands above to discover about filtering options to restrict hosts that checks will run against or to run a smaller set of defined checks.

## Check hosts filter

The hosts which the check applies to are defined using a variable named `__hosts_filter__`

Hosts filters can be applied at 2 levels

1. **⁠Module level** - At the top of the Python file
2. **⁠Class level** - Defined as a class attribute in a class which has check methods

The variable type annotation is `Callable[[Host], bool]`⁠, it expects a callable function which accepts a host parameter and should return True for a host that the check should execute against.

## Pytest Plugin

The nectl library ships with a pytest plugin which can be used to interact with hosts and facts in a kit.

The plugin defines a Pytest fixture named `host` which can be used within the test to interact with the host object that is being checked. Access to any of the hosts attributes, which are defined in the datatree, can be performed using dot notation. E.g `host.os_name`

The parametrize feature in pytest is used to pass in the host object to each check.

## Check examples

### Match all hosts

A single check which ensures that all hosts are running the same network OS and version.

```python
# demo-kit/checks/check_all.py

def check_os_name_is_junos(host):
    assert host.os_version == 'junos'

def check_os_version_is_recommended(host):
    assert host.os_version == '1.2.3'
```

### Match hosts in site

A check which will only run on hosts in the `newyork` site.

```python
# demo-kit/checks/check_newyork.py

__hosts_filter__ = lambda host: host.site == 'newyork'

def check_site(host):
    assert host.site == 'newyork'
```

### Check using classes

A check defined using a class which can be used to group checks and which can have its own hosts filter.

```python
# demo-kit/checks/check_junos.py

class CheckJunosHosts:
    __hosts_filter__ = lambda host: host.os_name == 'junos'
    
    def check_os_version(self, host):
        assert host.os_version == '1.2.3'
```