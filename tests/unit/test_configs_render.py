import pathlib
import pytest

from nectl.configs.render import render_hosts, render_template
from nectl.configs.templates import _import_template
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
        "func section_one():\n"
        "    print('foo')\n"
        "\n"
        "func section_two():\n"
        "    print('bar')\n"
    )

    # WHEN rendering template
    with pytest.raises(RenderError) as error:
        render_hosts(hosts=[host], config=config)

    # THEN expect error message
    assert "SyntaxError:" in str(error.value)


def test_should_return_no_hosts_when_rendering_host_with_no_os_name_defined(
    mock_config,
):
    # GIVEN mock config
    config = mock_config

    # GIVEN mock host with no os details provided
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        os_name=None,
        os_version=None,
    )

    # WHEN rendering hosts
    renders = render_hosts(hosts=[host], config=config)

    # THEN expect empty dict
    assert renders == {}


def test_should_return_config_when_rendering_template(mock_config):
    # GIVEN config
    config = mock_config

    # GIVEN facts
    facts = {
        "hostname": "fakenode",
        "os_name": "fakeos",
    }

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
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
        "fakeos", f"{config.kit_path}/{config.templates_dirname}"
    )

    # WHEN config is rendered
    render = render_template(template=template, facts=facts)

    # THEN
    assert render == "\n".join(
        ["top", "hostname is: fakenode", "middle", "os is fakeos", "end"]
    )
