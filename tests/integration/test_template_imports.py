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

from nectl.exceptions import TemplateImportError, TemplateMissingError
from nectl.configs.templates import get_template, _import_template


def test_should_return_correct_template_when_getting_template(mock_settings):
    # GIVEN mock settings
    settings = mock_settings

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
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

    # WHEN getting template using os
    template = get_template(os_name=os_name, settings=settings)

    # THEN expect template name
    assert template.__name__ == "fakeos"


def test_should_return_template_when_importing_template(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
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
        "fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_return_template_when_importing_template_in_subdir_using_slash(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname / "foodir"
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
        "foodir/fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_return_template_when_importing_template_in_subdir_using_dot(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN templates with subdirectory directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname / "foodir"
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
        "foodir.fakeos", f"{settings.kit_path}/{settings.templates_dirname}"
    )

    # THEN expect section one to exist in template
    assert "section_one" in dir(template)

    # THEN expect section two to exist in template
    assert "section_two" in dir(template)


def test_should_raise_error_when_getting_template_file_that_does_not_exist(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

    # GIVEN templates directory
    templates = pathlib.Path(settings.kit_path) / settings.templates_dirname
    templates.mkdir(parents=True)

    # GIVEN no template file is present

    # WHEN import template
    with pytest.raises(TemplateMissingError) as error:
        _import_template("fakeos", f"{settings.kit_path}/{settings.templates_dirname}")

    # THEN expect error message
    assert str(error.value) == "template import error with os_name: fakeos"


def test_should_raise_error_when_getting_template_that_is_invalid(
    mock_settings,
):
    # GIVEN settings
    settings = mock_settings

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

    # WHEN import template
    with pytest.raises(TemplateImportError) as error:
        _import_template("fakeos", f"{settings.kit_path}/{settings.templates_dirname}")

    # THEN expect error message
    assert "invalid syntax" in str(error.value)
