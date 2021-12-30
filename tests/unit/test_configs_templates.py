import pathlib
import pytest

from nectl.exceptions import TemplateImportError
from nectl.configs.templates import get_template, _import_template


def test_should_return_correct_template_when_getting_template(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template exists
    (templates / "fakeos.py").write_text(
        "def section_one():\n"
        "    print('foo')\n"
        "\n"
        "def section_two():\n"
        "    print('bar')\n"
    )

    # GIVEN host os name
    os_name = "fakeos"

    # GIVEN host os_version
    os_version = "5.1"

    # WHEN getting template using os and os_version
    template = get_template(os_name=os_name, os_version=os_version, config=config)

    # THEN expect template name
    assert template.__name__ == "fakeos"


def test_should_return_template_when_importing_template(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template exists
    (templates / "fakeos.py").write_text(
        "def section_one():\n"
        "    print('foo')\n"
        "\n"
        "def section_two():\n"
        "    print('bar')\n"
    )

    # WHEN import template
    template = _import_template(
        "fakeos", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_return_template_when_importing_template_in_subdir_using_slash(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname / "foodir"
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists
    (templates / "fakeos.py").write_text(
        "def section_one():\n"
        "    print('foo')\n"
        "\n"
        "def section_two():\n"
        "    print('bar')\n"
    )

    # WHEN import template
    template = _import_template(
        "foodir/fakeos", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_return_template_when_importing_template_in_subdir_using_dot(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname / "foodir"
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists
    (templates / "fakeos.py").write_text(
        "def section_one():\n"
        "    print('foo')\n"
        "\n"
        "def section_two():\n"
        "    print('bar')\n"
    )

    # WHEN import template
    template = _import_template(
        "foodir.fakeos", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_raise_error_when_getting_template_file_that_does_not_exist(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN no template file is present

    # WHEN import template
    with pytest.raises(TemplateImportError) as error:
        _import_template("fakeos", f"{config.kit_path}/{config.templates_dirname}")

    # THEN expect error message
    assert str(error.value) == "template file not found: fakeos"


def test_should_raise_error_when_getting_template_that_is_invalid(
    mock_config,
):
    # GIVEN config
    config = mock_config

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

    # WHEN import template
    with pytest.raises(TemplateImportError) as error:
        _import_template("fakeos", f"{config.kit_path}/{config.templates_dirname}")

    # THEN expect error message
    assert "invalid syntax" in str(error.value)
