import pytest
from unittest.mock import patch, MagicMock, call, mock_open

from nectl.configs.drivers import NapalmDriver
from nectl.datatree.hosts import Host
from nectl.exceptions import (
    DriverCommitDisconnectError,
    DriverConfigLoadError,
    DriverError,
    DriverNotFoundError,
)
from napalm.base.exceptions import (
    ModuleImportError,
    LockError,
    ConnectionException,
    MergeConfigException,
    ReplaceConfigException,
)
from ncclient.transport.errors import AuthenticationError


@pytest.fixture
def mock_napalm(monkeypatch):
    """Fixture that will mock 'my_module.foo' and return the mock."""
    mock_driver = MagicMock()
    monkeypatch.setattr(
        "nectl.configs.drivers.napalmdriver.get_network_driver",
        MagicMock(return_value=mock_driver)
        # MagicMock(return_value=MagicMock(return_value=mock_driver)),
    )
    return mock_driver


def test_should_open_and_close_connection_when_using_context_manager(
    mock_napalm,
):
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # WHEN connection opened
    with driver:
        # THEN expect napalm open to be called but not close
        mock_napalm.return_value.open.assert_called()
        mock_napalm.return_value.close.assert_not_called()

    # THEN expect napalm close to be called
    mock_napalm.return_value.close.assert_called()


def test_should_return_config_when_getting_config(mock_napalm):
    # GIVEN mock config
    mock_config = "set foo bar"

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="testuser")

    # GIVEN internal driver calls are patched
    mock_napalm.return_value.get_config.return_value = {"running": mock_config}

    # WHEN getting config
    with driver:
        config = driver.get_config(format="cli", sanitized=True)

    # THEN expect get_config to be called
    mock_napalm.return_value.get_config.assert_called()

    # THEN expect get_config args to be supplied
    mock_napalm.return_value.get_config.assert_called_with(
        retrieve="running", sanitized=True
    )

    # THEN expect config to match mock config
    assert config == mock_config


@patch("builtins.open", new_callable=mock_open, read_data=None)
@pytest.mark.parametrize(
    "os_name,format,config",
    (
        ("eos", "cli", "hostname core0"),
        ("junos", "set", "set system host-name core0"),
        ("junos", "text", "system { host-name core0; }"),
    ),
)
def test_should_replace_config_unless_using_junos_set_config_format(
    mock_open, mock_napalm, os_name, format, config
):
    # GIVEN format and config
    format = format
    config = config

    # GIVEN fake config file path
    config_filepath = "/not/real/config.txt"

    # GIVEN open file returns config
    open.return_value.read.return_value = config

    # GIVEN host with os_name
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name=os_name,
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN diff
    mock_napalm.return_value.compare_config.return_value = "fakediff"

    # WHEN calling compare config
    with driver:
        diff = driver.compare_config(config_filepath=config_filepath)

    # THEN if junos os and set format
    if os_name == "junos" and format == "set":
        mock_napalm.return_value.load_merge_candidate.assert_has_calls(
            [
                call(config="delete"),
                call(config=config),
            ]
        )

    # THEN for all other os_names and formats
    else:
        mock_napalm.return_value.load_replace_candidate.assert_called_once_with(
            config=config
        )

    # THEN expect compare method to be called
    mock_napalm.return_value.compare_config.assert_called()

    # THEN expect diff to match
    assert diff == "fakediff"


@pytest.mark.parametrize(
    "napalm_exc,driver_exc",
    (
        (ModuleImportError(), DriverNotFoundError),
        (LockError(), DriverError),
        (AuthenticationError(), DriverError),
        (ConnectionException(), DriverError),
    ),
)
def test_should_raise_error_when_driver_open(mock_napalm, napalm_exc, driver_exc):
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN napalm open method that raises our exception
    mock_napalm.return_value.open.side_effect = napalm_exc

    # THEN expect driver exception
    with pytest.raises(driver_exc):
        # WHEN driver opens
        with driver:
            pass


def test_should_not_raise_error_when_driver_close(mock_napalm, caplog):
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN napalm close method that raises our exception
    mock_napalm.return_value.close.side_effect = ConnectionException

    # WHEN driver opens and then closes
    with driver:
        pass

    # THEN expect no error to be raised but warning log
    assert "error closing connection: ConnectionException" in caplog.text


@patch("builtins.open", new_callable=mock_open, read_data=None)
@pytest.mark.parametrize(
    "napalm_exc,driver_exc",
    (
        (FileNotFoundError(), DriverConfigLoadError),
        (MergeConfigException(), DriverConfigLoadError),
        (ReplaceConfigException(), DriverConfigLoadError),
    ),
)
def test_should_raise_error_when_comparing_config(
    mock_open, mock_napalm, napalm_exc, driver_exc
):
    # GIVEN open file returns string
    open.return_value.read.return_value = ""

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN napalm compare_method that raises our exception
    mock_napalm.return_value.compare_config.side_effect = napalm_exc

    # THEN expect driver exception
    with pytest.raises(driver_exc):
        # WHEN calling compare config
        with driver:
            driver.compare_config("/mock/config.txt")


@patch("builtins.open", new_callable=mock_open, read_data=None)
def test_should_return_diff_and_not_commit_when_applying_config_but_no_changes(
    mock_open,
    mock_napalm,
):
    # GIVEN open file returns string
    open.return_value.read.return_value = ""

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN compare method will return None
    mock_napalm.return_value.compare_config.return_value = None

    # WHEN calling apply config
    with driver:
        diff = driver.apply_config(config_filepath="/not/real/config.txt", format="set")

    # THEN expect config compare method to be called
    mock_napalm.return_value.compare_config.assert_called()

    # THEN expect commit not to be called
    mock_napalm.return_value.commit_config.assert_not_called()

    # THEN expect diff to be blank
    assert diff == None


@patch("time.sleep")
@patch("builtins.open", new_callable=mock_open, read_data=None)
def test_should_return_diff_and_commit_when_replacing_config_and_has_changes(
    mock_open, mock_sleep, mock_napalm
):
    # GIVEN open file returns string
    open.return_value.read.return_value = ""

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN compare method will return changes
    mock_napalm.return_value.compare_config.return_value = "fakediff"

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # WHEN calling apply config
    with driver:
        diff = driver.apply_config(
            config_filepath="/not/real/config.txt", commit_timer=10
        )

    # THEN expect config compare method to be called
    mock_napalm.return_value.compare_config.assert_called()

    # THEN expect commit to be called
    mock_napalm.return_value.commit_config.assert_called()

    # THEN expect mgmt connection to be restarted
    mock_napalm.return_value.close.assert_called()

    # THEN expect sleep for 75% of 10 minutes = 450 seconds
    mock_sleep.assert_called_with(450)

    # THEN expect commit to be confirmed
    mock_napalm.return_value.confirm_commit.assert_called()

    # THEN expect diff to be returned
    assert diff == "fakediff"


@patch("builtins.open", new_callable=mock_open, read_data=None)
def test_should_raise_error_when_replacing_config_and_host_connection_lost(
    mock_open, mock_napalm
):
    # GIVEN open file returns string
    open.return_value.read.return_value = ""

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="10.0.0.1",
        os_name="junos",  # junos is irrelevant just needs to be a valid driver
        _facts={},
        _settings=None,
    )

    # GIVEN driver
    driver = NapalmDriver(host=host, username="foo")

    # GIVEN compare method will return changes
    mock_napalm.return_value.compare_config.return_value = "fakediff"

    # GIVEN commit method will raise error
    mock_napalm.return_value.commit_config.side_effect = ConnectionException("foo")

    with pytest.raises(DriverCommitDisconnectError) as error:
        # WHEN calling apply config
        with driver:
            driver.apply_config(config_filepath="/not/real/config.txt", commit_timer=10)

    # THEN expect error message
    assert (
        str(error.value)
        == "host connection lost after commit: ConnectionException: foo"
    )
