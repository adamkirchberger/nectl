import pathlib
import pytest

from nectl.templates.render import render_hosts
from nectl.data.hosts import Host
from nectl.exceptions import RenderError


def test_should_raise_error_when_rendering_with_no_blueprints_map_defined(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN blueprints_map is blank
    config.blueprints_map = {}

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
        == "templates cannot be rendered when 'blueprints_map' is not defined."
    )


def test_should_raise_render_error_when_rendering_with_invalid_blueprint(mock_config):
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

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir(parents=True)

    # GIVEN fakeos blueprint exists but is invalid
    (blueprints / "fakeos.py").write_text(
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
