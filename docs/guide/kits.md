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

# Kits

## Summary

A kit is a directory which stores data that is unique for a single network environment. The kit concept exists to decouple the user data from the tool, allowing users to define as many kits as required with respective data, settings and customisations.

Nectl will read the kit in the current working directory and perform actions based on the arguments that are passed to the CLI tool.

## What is in a kit

- `nectl.yaml`: Settings for the kit.
- `models`: Data models used in the datatree.
- `data`: Holds the datatree which is used to define host facts.
- `templates`: Configuration templates using datatree and models.
- `configs`: Configuration renders, diffs and backups are saved.
- `checks`: Pre and Post checks to run on hosts.
- `drivers`: Optional custom drivers.

## Kit Scope

A kit should be kept in version control using Git or other similar tools, to easily track and control all changes made to a network environment.

**A kit can be configured for**

- A single site.
- Multiple sites.
- Multiple customers and sites.

How this is done is defined in the settings file and can be completely customised to fit your environment.

A good approach is to split up the kits based on administrative domain as this provides a simple method to control user privileges by using Git repo permissions.

Although it may seem best to split environments into many small kits, a balance needs to be found to ensure that common data is not unnecessarily being duplicated across many kits as this can lead to inconsistencies and time consuming rollouts.
