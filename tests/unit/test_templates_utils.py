import pathlib
import pytest

from nectl.exceptions import BlueprintImportError
from nectl.templates.utils import get_blueprint, _import_blueprint


def test_should_return_correct_blueprint_when_getting_blueprint(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir()

    # GIVEN fakeos blueprint exists with FakeOs class
    (blueprints / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # GIVEN host os
    os = "fakeos"

    # GIVEN host os_version
    os_version = "5.1"

    # WHEN getting blueprint using os and os_version
    blueprint = get_blueprint(config, host_os=os, host_os_version=os_version)

    # THEN expect blueprint name
    assert blueprint.__name__ == "FakeOs"


def test_should_return_blueprint_when_importing_blueprint(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir()

    # GIVEN fakeos blueprint exists with FakeOs class
    (blueprints / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import blueprint
    blueprint = _import_blueprint(
        "fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
    )

    # THEN expect calling test method to return value
    assert blueprint.test_method() == "foo"


def test_should_return_blueprint_when_importing_blueprint_in_subdir_using_slash(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints with subdirectory directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname / "foodir"
    blueprints.mkdir(parents=True)

    # GIVEN fakeos blueprint exists with FakeOs class
    (blueprints / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import blueprint
    blueprint = _import_blueprint(
        "foodir/fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
    )

    # THEN expect calling test method to return value
    assert blueprint.test_method() == "foo"


def test_should_return_blueprint_when_importing_blueprint_in_subdir_using_dot(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints with subdirectory directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname / "foodir"
    blueprints.mkdir(parents=True)

    # GIVEN fakeos blueprint exists with FakeOs class
    (blueprints / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import blueprint
    blueprint = _import_blueprint(
        "foodir.fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
    )

    # THEN expect calling test method to return value
    assert blueprint.test_method() == "foo"


def test_should_raise_error_when_getting_blueprint_file_that_does_not_exist(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir(parents=True)

    # GIVEN no blueprint file is present

    # WHEN import blueprint
    with pytest.raises(BlueprintImportError) as error:
        _import_blueprint(
            "fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
        )

    # THEN expect error message
    assert str(error.value) == "blueprint file not found: fakeos"


def test_should_raise_error_when_getting_blueprint_class_that_does_not_exist(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir(parents=True)

    # GIVEN fakeos blueprint exists with a different class
    (blueprints / "fakeos.py").write_text(
        "class WrongName:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import blueprint
    with pytest.raises(BlueprintImportError) as error:
        _import_blueprint(
            "fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
        )

    # THEN expect error message
    assert str(error.value) == "blueprint 'fakeos' class not found named: FakeOs"


def test_should_raise_error_when_getting_blueprint_class_that_is_invalid(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN blueprints directory
    blueprints = pathlib.Path(config.kit_path) / config.blueprints_dirname
    blueprints.mkdir(parents=True)

    # GIVEN fakeos blueprint exists but is invalid
    (blueprints / "fakeos.py").write_text(
        "INVALIDCLASS WrongName:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import blueprint
    with pytest.raises(BlueprintImportError) as error:
        _import_blueprint(
            "fakeos:FakeOs", f"{config.kit_path}/{config.blueprints_dirname}"
        )

    # THEN expect error message
    assert "SyntaxError:" in str(error.value)
