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

from nectl.exceptions import TemplateImportError
from nectl.configs.templates import get_template, _import_template


def test_should_return_correct_template_when_getting_template(mock_config):
    # GIVEN mock config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template exists with FakeOs class
    (templates / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # GIVEN host os name
    os_name = "fakeos"

    # GIVEN host os_version
    os_version = "5.1"

    # WHEN getting template using os and os_version
    template = get_template(os_name=os_name, os_version=os_version, config=config)

    # THEN expect template name
    assert template.__name__ == "FakeOs"


def test_should_return_template_when_importing_template(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir()

    # GIVEN fakeos template exists with FakeOs class
    (templates / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import template
    template = _import_template(
        "fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect calling test method to return value
    assert template.test_method() == "foo"


def test_should_return_template_when_importing_template_in_subdir_using_slash(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname / "foodir"
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists with FakeOs class
    (templates / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import template
    template = _import_template(
        "foodir/fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect calling test method to return value
    assert template.test_method() == "foo"


def test_should_return_template_when_importing_template_in_subdir_using_dot(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname / "foodir"
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists with FakeOs class
    (templates / "fakeos.py").write_text(
        "class FakeOs:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import template
    template = _import_template(
        "foodir.fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
    )

    # THEN expect calling test method to return value
    assert template.test_method() == "foo"


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
        _import_template(
            "fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
        )

    # THEN expect error message
    assert str(error.value) == "template file not found: fakeos"


def test_should_raise_error_when_getting_template_class_that_does_not_exist(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists with a different class
    (templates / "fakeos.py").write_text(
        "class WrongName:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import template
    with pytest.raises(TemplateImportError) as error:
        _import_template(
            "fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
        )

    # THEN expect error message
    assert str(error.value) == "template 'fakeos' class not found named: FakeOs"


def test_should_raise_error_when_getting_template_class_that_is_invalid(
    mock_config,
):
    # GIVEN config
    config = mock_config

    # GIVEN templates directory
    templates = pathlib.Path(config.kit_path) / config.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN fakeos template exists but is invalid
    (templates / "fakeos.py").write_text(
        "INVALIDCLASS WrongName:\n"
        "    def __init__(self):\n"
        "        pass\n"
        "    @staticmethod\n"
        "    def test_method():\n"
        "        return 'foo'\n"
    )

    # WHEN import template
    with pytest.raises(TemplateImportError) as error:
        _import_template(
            "fakeos:FakeOs", f"{config.kit_path}/{config.templates_dirname}"
        )

    # THEN expect error message
    assert "SyntaxError:" in str(error.value)