# Copyright (C) 2021 Adam Kirchberger
#
# This file is part of Nectl.
#
# Nectl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Nectl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Nectl.  If not, see <http://www.gnu.org/licenses/>.

class ConfigFileError(Exception):
    """
    Indicates that errors have been encountered related to config file.
    """


class RenderError(Exception):
    """
    Indicates that render of hosts has encountered an error.
    """


class TemplateMissingError(Exception):
    """
    Indicates that no suitable template has been found for host.
    """


class TemplateImportError(Exception):
    """
    Indicates that template file does not exist or has errors.
    """
