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


class Actions:
    """
    Actions are used as type hints to tell nectl how facts should be loaded

    Examples:
        from nectl import actions

        # overwritten if defined at more specific level
        my_var: actions.replace_with = "new value"

        # merge action for lists and dictionaries
        my_var: actions.merge_with = ["appended value"]

        # frozen will hold on to the first value
        my_var: actions.frozen = "protected value"
    """

    replace_with = "replace_with"
    merge_with = "merge_with"
    frozen = "frozen"
