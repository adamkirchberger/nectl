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

# Host Configs Usage

The network control CLI tool provides the following actions for working with host configurations.

?> All logs are written to `nectl.log` at the root of your network kit. To log events to the terminal use `-v`, additional `v`'s will increase the verbosity.

## Render Configs

Use this to generate host configs from templates.

**The steps are:**

1. Discover hosts from the datatree.
1. Fetch host facts using the datatree inheritance.
1. Look for a template based on the host `os_name` value.
1. Render sections in the template.
1. Write staged config to kit. (defaults to `demo-kit/configs/staged`)

```bash
# Render configs for all hosts
nectl configs render

# Render configs for single site
nectl configs render --site ldn

# Render configs for single host
nectl configs render --site ldn --hostname firewall1
```

## Compare Configs

Use this to compare a staged configuration, rendered by _nectl_, to the active configuration on the host and produce a diff file.

!> Note that this action will not render configs so staged configs must exist (by running the render action above first) or an error will be raised.

**The steps are:**

1. Discover hosts from the datatree.
1. Check that staged configs exist for hosts.
1. Look for a driver based on the host `os_name` value.
1. Open connection to host using the driver.
1. Request that driver compare staged and active config.
1. Write diff files to kit. (defaults to `demo-kit/configs/diffs`)

```bash
# Compare configs for all hosts
nectl configs diff

# Compare configs for single site
nectl configs diff --site ldn

# Compare configs for single host
nectl configs diff --site ldn --hostname firewall1
```

## Apply Config

Use this to deploy staged configs,rendered by _nectl_, onto live hosts.

!> **MUST READ!**</br></br>
**This action can be disruptive and cause potential outages** if changes have not been tested properly. Make sure to test changes on a lab host first and always perform a _compare_ to review any diff files before an _apply_ action.

!> Note that this action will not render configs so staged configs must exist (by running the render action above first) or an error will be raised.

**The steps are:**

1. Discover hosts from the datatree.
1. Check that staged configs exist for hosts.
1. Look for a driver based on the host `os_name` value.
1. Open connection to host using the driver.
1. Request that driver compare staged and active config.
1. If there are no changes required then exit else continue.
1. Push configuration to device.
1. Run commit checks.
1. Commit configuration with automated rollback.
1. Disconnect and reconnect to device to confirm MGMT IP access.
1. Confirm commit.
1. Write diff files to kit. (defaults to `demo-kit/configs/diffs`)

?> The commit check and rollback steps may or may not exist as these are dependent on how the OS specific driver is implemented.

```bash
# Apply configs for all hosts
nectl configs apply

# Apply configs for single site
nectl configs apply --site ldn

# Apply configs for single host
nectl configs apply --site ldn --hostname firewall1
```
