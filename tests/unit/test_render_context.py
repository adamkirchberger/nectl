# Copyright (C) 2022 Adam Kirchberger
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

from nectl.configs.render import _render_context
from nectl.configs.template_utils import get_render_facts


def test_should_return_empty_dict_when_returning_host_facts_with_default_context():
    # GIVEN that we are not running in a template and render context is blank

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to be empty dict
    assert facts == {}


def test_should_return_empty_dict_when_returning_host_facts_with_context_set():
    # GIVEN mock facts
    mock_facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN that context has been set with facts
    _render_context.set({"facts": mock_facts})

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to match mock facts
    assert facts == mock_facts

    # GIVEN that we are not running in a template and render context is blank

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to be empty dict
    assert facts == {}


def test_should_return_empty_dict_when_returning_host_facts_with_context_set():
    # GIVEN mock facts
    mock_facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN that context has been set with facts
    _render_context.set({"facts": mock_facts})

    # WHEN getting facts
    facts = get_render_facts()

    # THEN expect result to match mock facts
    assert facts == mock_facts
