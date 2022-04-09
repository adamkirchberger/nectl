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

import os
import pathlib
import pytest

from nectl.configs.render import render_hosts, render_template
from nectl.configs.templates import _import_template
from nectl.configs.utils import write_configs_to_dir
from nectl.datatree.hosts import Host
from nectl.exceptions import RenderError


def test_should_return_config_dict_when_rendering_with_valid_template(mock_settings):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN mock host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name="fakeos",
        os_version="5.1",
        _settings=settings,
    )

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists
    (templates / "fakeos.py").write_text(
        "def section_one(hostname):\n"
        "    print(f'hostname is: {hostname}')\n"
        "\n"
        "def section_two(site):\n"
        "    print(f'site is: {site}')\n"
    )

    # WHEN rendering hosts
    configs = render_hosts(hosts=[host], settings=settings)

    # THEN expect to be dict
    assert isinstance(configs, dict)

    # THEN expect host to be in configs
    assert host.id in configs.keys()

    # THEN expect host config
    assert configs.get(host.id) == "hostname is: core0\nsite is: london"


def test_should_raise_render_error_when_rendering_with_invalid_template(mock_settings):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN mock host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name="fakeos",
        os_version="5.1",
        _settings=settings,
    )

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists but is invalid
    (templates / "fakeos.py").write_text(
        "func section_one():\n"
        "    print('foo')\n"
        "\n"
        "func section_two():\n"
        "    print('bar')\n"
    )

    # WHEN rendering hosts
    with pytest.raises(RenderError) as error:
        render_hosts(hosts=[host], settings=settings)

    # THEN expect error message
    assert "invalid syntax" in str(error.value)


def test_should_return_no_hosts_when_rendering_host_with_no_os_name_defined(
    mock_settings,
):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN mock host with blank os details provided
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name=None,
        os_version=None,
        _facts={},  # patch facts to avoid 'os_name' lookup in datatree
    )

    # WHEN rendering hosts
    renders = render_hosts(hosts=[host], settings=settings)

    # THEN expect empty dict
    assert renders == {}


def test_should_return_config_when_rendering_template(mock_settings):
    # GIVEN settings
    settings = mock_settings

    # GIVEN facts
    facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template file with non alphabetically sorted section names
    #       to test that order of definition is honored
    (templates / "fakeos.py").write_text(
        "def display_1(hostname):\n"
        "    print('top')\n"
        "    print(f'hostname is: {hostname}')\n"
        "\n"
        "def display_3(os_name):\n"
        "    print('middle')\n"
        "    print(f'os is {os_name}')\n"
        "\n"
        "def display_2():\n"
        "    print('end')\n"
    )

    # GIVEN template module
    template = _import_template(
        "fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # WHEN config is rendered
    render = render_template(template=template, facts=facts)

    # THEN expect config section order based on how they are defined in code
    assert render == "\n".join(
        ["top", "hostname is: fakenode", "middle", "os is fakeos", "end"]
    )


def test_should_return_config_with_default_arg_value_when_rendering_template(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN facts
    facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir()

    # GIVEN template with one section which has optional variable 'location'
    (templates / "fakeos.py").write_text(
        "def section_one(hostname, location='default_location'):\n"
        "    print(f'hostname is: {hostname}')\n"
        "    print(f'location is: {location}')\n"
    )

    # GIVEN template module
    template = _import_template(
        "fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # WHEN config is rendered
    render = render_template(template=template, facts=facts)

    # THEN expect render to use default location value
    assert render == "\n".join(
        ["hostname is: fakenode", "location is: default_location"]
    )


def test_should_raise_error_when_rendering_template_with_required_variable_that_is_not_in_facts(
    mock_settings, caplog
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN facts
    facts = {
        "id": "fakenode.fakesite",
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir()

    # GIVEN template file with section that requires fact 'location'
    (templates / "fakeos.py").write_text(
        "def section_one(hostname, location):\n"
        "    print(f'hostname is: {hostname}')\n"
        "    print(f'location is: {location}')\n"
    )

    # GIVEN template module
    template = _import_template(
        "fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # WHEN config is rendered
    with pytest.raises(RenderError) as error:
        render_template(template=template, facts=facts)

    # THEN expect error to have been raised with message
    assert (
        str(error.value)
        == "render aborted due to 1 render errors with host: fakenode.fakesite"
    )

    # THEN expect to have log with detailed error
    assert "template 'fakeos:section_one' needs fact: 'location'" in caplog.text


def test_should_raise_error_when_rendering_template_which_encounters_unexpected_error(
    mock_settings, caplog
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN facts
    facts = {
        "id": "fakenode.fakesite",
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir()

    # GIVEN template file with section that performs invalid addition on string
    (templates / "fakeos.py").write_text(
        "def section_one(hostname):\n" "    print(f'hostname is: {hostname+100}')\n"
    )

    # GIVEN template module
    template = _import_template(
        "fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # WHEN config is rendered
    with pytest.raises(RenderError) as error:
        render_template(template=template, facts=facts)

    # THEN expect error to have been raised with message
    assert (
        str(error.value)
        == "render aborted due to 1 render errors with host: fakenode.fakesite"
    )

    # THEN expect to have log with detailed error
    assert (
        "template 'fakeos:section_one' unknown error: can only concatenate str"
        in caplog.text
    )


def test_should_return_config_when_rendering_template_that_has_conditional_imports_of_sub_templates(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN host with model facts
    host = Host(
        hostname="fakenode",
        site="london",
        os_name="fakeos",
        os_version="1.2.3",
        _facts={"hostname": "fakenode", "model": "az"},  # patch facts to avoid lookup
    )

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template is a directory of templates
    (templates / "fakeos").mkdir()

    # GIVEN main template which imports sub templates
    (templates / "fakeos" / "__init__.py").write_text(
        "import nectl.configs.template_utils\n"
        "\n"
        "if nectl.configs.template_utils.get_render_facts().get('model') == 'az':\n"
        "    from .az_subtemplate import *\n"
        "\n"
        "def base_section(hostname):\n"
        "    print(f'hostname is: {hostname}')\n"
    )

    # GIVEN main template which imports two sub templates
    (templates / "fakeos" / "az_subtemplate.py").write_text(
        "def az_section_one():\n"
        "    print('start of az template')\n"
        "\n"
        "def az_section_two(model):\n"
        "    print(f'model is: {model}')\n"
    )

    # GIVEN expected config
    expected_config = "start of az template\n" "model is: az\n" "hostname is: fakenode"

    # WHEN rendering hosts
    configs = render_hosts(hosts=[host], settings=settings)

    # THEN expect config for host to match expected config
    assert configs["fakenode.london"] == expected_config


def test_should_return_config_when_writing_configs_to_files(mock_settings):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN output directory
    output_dir = f"{settings.kit_path}/{settings.staged_configs_dir}"

    # GIVEN mock rendered configs
    rendered_configs = {
        "host1": "config for host1",
        "host2": "config for host2",
        "host3": "config for host3",
    }

    # WHEN writing configs to staged output dir
    write_configs_to_dir(configs=rendered_configs, output_dir=output_dir)

    # THEN expect there to be 3 files written
    assert len(os.listdir(output_dir))

    # THEN expect each host file to have content
    for host, conf in rendered_configs.items():
        with open(f"{output_dir}/{host}.txt", "r") as fh:
            assert fh.read() == conf + "\n"
