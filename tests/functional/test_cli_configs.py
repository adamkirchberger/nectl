import pytest
import click

import nectl.config
from nectl.cli import cli_root


@pytest.mark.parametrize("command", ["list-templates"])
def test_should_raise_error_when_running_cli_configs_unimplemented_commands(
    cli_runner, mock_config, command
):
    # GIVEN command args
    args = ["configs", command]

    # GIVEN get_config() is patched to return mock_config
    nectl.config.__config = mock_config

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be unsuccessful
    assert result.exit_code == 1

    # THEN expect not implemented error
    assert isinstance(result.exception, NotImplementedError)


def test_should_return_config_when_running_cli_configs_render_command(
    cli_runner, mock_config, mock_template_generator
):
    # GIVEN args
    args = ["configs", "render", "-h", "core0", "-s", "london", "-c", "acme"]

    # GIVEN expected output config
    config = (
        "host: core0.london.acme\n"
        "hostname is: core0\n"
        "os_name is: fakeos\n"
        "template end\n"
    )

    # GIVEN get_config() is patched to return mock_config
    nectl.config.__config = mock_config

    # GIVEN template exists in kit directory
    mock_template_generator(mock_config)

    # WHEN cli command is run
    result = cli_runner.invoke(cli_root, args)

    # THEN expect to be successful
    assert result.exit_code == 0

    # THEN expect output
    assert config in result.output
