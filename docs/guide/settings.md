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

# Settings

## Summary

The settings for a kit are defined in a configuration file. All kits must have a settings file to define the values for options which are outlined below.

The settings file should be version controlled with the kit.

## Settings File

The settings will be found in two ways

1. Automatically in the root of the kit in a file called `kit.py`.

2. Using environment variable `NECTL_KIT` that has path to settings file.

## Options

For example settings files and values see [Quick start](quickstart.md)

| **Name**               | **Required** | **Default**    | **Description**                                                                                       |
| ---------------------- | ------------ | -------------- | ----------------------------------------------------------------------------------------------------- |
| datatree_lookup_paths  | Yes          |                | List of datatree inheritance lookup paths.                                                            |
| hosts_glob_pattern     | Yes          |                | Glob pattern to find all hosts.                                                                       |
| hosts_hostname_regex   | Yes          |                | Regex pattern used to pull hostname from host file path.                                              |
| hosts_site_regex       | Optional     | None           | Regex pattern used to pull site from host file path.                                                  |
| hosts_customer_regex   | Optional     | None           | Regex pattern used to pull customer from host file path.                                              |
| datatree_dirname       | Optional     | data           | Datatree default directory name.                                                                      |
| templates_dirname      | Optional     | templates      | Templates default directory name.                                                                     |
| drivers_dirname        | Optional     | drivers        | Custom drivers directory name.<br>Note that these will override library drivers if same name is used. |
| default_action         | Optional     | replace_with   | Default data action.                                                                                  |
| staged_configs_dir     | Optional     | configs/staged | Default rendered configs output directory.                                                            |
| config_diffs_dir       | Optional     | configs/diffs  | Default configs diffs directory.                                                                      |
| active_configs_dir     | Optional     | configs/active | Default active configs directory.                                                                     |
| configs_file_extension | Optional     | txt            | Default configs file extension.                                                                       |
| configs_format         | Optional     |                | Config format variable passed to driver methods.                                                      |
| configs_sanitized      | Optional     | True           | Defines whether configs pulled from devices should be sanitized.                                      |
| default_driver         | Optional     | None           | Defines a default driver if one is not found. Test and use at own risk!                               |
