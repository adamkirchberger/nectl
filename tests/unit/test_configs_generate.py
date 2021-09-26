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

import pathlib
import pytest

from nectl.configs.render import render_hosts
from nectl.data.hosts import Host
from nectl.exceptions import RenderError


def test_should_raise_error_when_rendering_with_no_templates_map_defined(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN templates_map is blank
    config.templates_map = {}

    # GIVEN mock host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name="fakeos",
        os_version="5.1",
    )

    # WHEN rendering template
    with pytest.raises(RenderError) as error:
        render_hosts(hosts=[host], config=config)

    # THEN expect error message
    assert (
        str(error.value)
        == "templates cannot be rendered when 'templates_map' is not defined."
    )


def test_should_raise_render_error_when_rendering_with_invalid_template(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN mock host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name="fakeos",
        os_version="5.1",
    )

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists but is invalid
    (templates / "fakeos.py").write_text(
        "INVALIDCLASS FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN rendering template
    with pytest.raises(RenderError) as error:
        render_hosts(hosts=[host], config=config)

    # THEN expect error message
    assert "SyntaxError:" in str(error.value)
