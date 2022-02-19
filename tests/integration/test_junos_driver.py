import pytest
from unittest.mock import patch, MagicMock, call

from nectl.configs.drivers import JunosDriver
from nectl.data.hosts import Host
from nectl.exceptions import (
    DriverCommitDisconnectError,
    DriverConfigLoadError,
    DriverError,
)
from jnpr.junos.exception import (
    LockError,
    ConfigLoadError,
    CommitError,
    RpcTimeoutError,
)


@patch("jnpr.junos.Device.open")
@patch("jnpr.junos.Device.close")
def test_should_open_and_close_connection_when_using_context_manager(
    mock_junos_close, mock_junos_open
):
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")

    # WHEN connection opened
    with junos_driver:
        # THEN expect junos open to be called but not close
        mock_junos_open.assert_called()
        mock_junos_close.assert_not_called()

    # THEN expect junos close to be called
    mock_junos_close.assert_called()


def test_should_return_config_when_getting_junos_config():
    # GIVEN mock config
    mock_config = "set foo bar"

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN junos driver
    junos_driver = JunosDriver(host=host, username="testuser")

    # GIVEN internal driver calls are patched
    mock_driver = MagicMock(return_value=None)
    mock_driver.rpc.get_config.return_value.text.return_value = mock_config
    junos_driver._driver = mock_driver

    # WHEN getting config
    config = junos_driver.get_config(format="set")

    # THEN expect get_config to be called
    mock_driver.rpc.get_config.assert_called()

    # THEN expect get_config args to be supplied
    mock_driver.rpc.get_config.assert_called_with(options={"format": "set"})

    # THEN expect config to match mock config
    assert config.return_value == mock_config


@pytest.mark.parametrize("format", ("set", "json", "xml"))
def test_should_claim_lock_when_comparing_config(
    format,
):
    # GIVEN fake config file path
    config_filepath = "/not/real/config.txt"

    # GIVEN config format
    format = format

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")
    junos_driver._driver = MagicMock(return_value=None)  # mocked connection

    # GIVEN driver is mocked to be connected
    JunosDriver.is_connected = True

    # GIVEN diff
    junos_driver._driver.cu.diff.return_value = "fakediff"

    # WHEN calling compare config
    diff = junos_driver.compare_config(config_filepath=config_filepath, format=format)

    # THEN if format is "set" expect load calls
    if format == "set":
        junos_driver._driver.cu.load.assert_has_calls(
            [
                call("delete", format="set", merge=True),
                call(path=config_filepath, format="set", merge=True),
            ]
        )

    # THEN if format is not "set" expect load calls
    else:
        junos_driver._driver.cu.load.assert_called_once_with(
            path=config_filepath, update=True
        )

    # THEN expect config check method to be called
    junos_driver._driver.cu.commit_check.assert_called()

    # THEN expect config diff method to be called
    junos_driver._driver.cu.diff.assert_called()

    # THEN expect diff to match
    assert diff == "fakediff"


@pytest.mark.parametrize(
    "driver_error_method,junos_exc,driver_exc",
    (
        ("cu.lock", LockError(None), DriverError),
        ("cu.lock", FileNotFoundError(), DriverConfigLoadError),
        (
            "cu.lock",
            ConfigLoadError(None, errs=[{"message": "foo", "severity": "bar"}]),
            DriverConfigLoadError,
        ),
        (
            "cu.lock",
            CommitError(None, errs=[{"message": "foo", "severity": "bar"}]),
            DriverConfigLoadError,
        ),
    ),
)
def test_should_raise_error_when_comparing_config(
    driver_error_method, junos_exc, driver_exc
):
    # GIVEN driver error method which raises error
    driver_error_method = driver_error_method

    # GIVEN junos exception
    junos_exc = junos_exc

    # GIVEN driver exception
    driver_exc = driver_exc

    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")

    # GIVEN driver which has method that raises junos exception
    junos_driver._driver = MagicMock(
        return_value=None, **{f"{driver_error_method}.side_effect": junos_exc}
    )

    # GIVEN driver is mocked to be connected
    JunosDriver.is_connected = True

    # THEN expect driver exception
    with pytest.raises(driver_exc):
        # WHEN calling compare config
        junos_driver.compare_config("/mock/config.txt")


def test_should_return_diff_and_not_commit_when_replacing_config_but_no_changes():
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")
    junos_driver._driver = MagicMock(return_value=None)  # mocked connection

    # GIVEN driver is mocked to be connected
    JunosDriver.is_connected = True

    # GIVEN diff method will return None
    junos_driver._driver.cu.diff.return_value = None

    # WHEN calling replace config
    diff = junos_driver.replace_config(
        config_filepath="/not/real/config.txt", format="set"
    )

    # THEN expect config check method to be called
    junos_driver._driver.cu.commit_check.assert_called()

    # THEN expect config diff method to be called
    junos_driver._driver.cu.diff.assert_called()

    # THEN expect commit not to be called
    junos_driver._driver.cu.commit.assert_not_called()

    # THEN expect diff to be blank
    assert diff == None


@patch("time.sleep")
def test_should_return_diff_and_commit_when_replacing_config_and_has_changes(
    mock_sleep,
):
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")
    junos_driver._driver = MagicMock(return_value=None)  # mocked connection

    # GIVEN driver is mocked to be connected
    JunosDriver.is_connected = True

    # GIVEN diff method will return changes
    junos_driver._driver.cu.diff.return_value = "fakediff"

    # WHEN calling replace config
    diff = junos_driver.replace_config(
        config_filepath="/not/real/config.txt", format="set", commit_timer=10
    )

    # THEN expect config check method to be called
    junos_driver._driver.cu.commit_check.assert_called()

    # THEN expect config diff method to be called
    junos_driver._driver.cu.diff.assert_called()

    # THEN expect commit to be called
    junos_driver._driver.cu.commit.assert_called()

    # THEN expect mgmt connection to be restarted
    junos_driver._driver.close.assert_called()

    # THEN expect sleep for 75% of 10 minutes = 450 seconds
    mock_sleep.assert_called_with(450)

    # THEN expect commit to be confirmed
    assert junos_driver._driver.cu.commit_check.call_count == 2

    # THEN expect diff to be returned
    assert diff == "fakediff"


def test_should_raise_error_when_replacing_config_and_host_connection_lost():
    # GIVEN host
    host = Host(
        hostname="core0",
        site="london",
        customer="acme",
        mgmt_ip="x.x.x.x",
        _facts={},
        _config=None,
    )

    # GIVEN driver
    junos_driver = JunosDriver(host=host, username="foo")
    junos_driver._driver = MagicMock(return_value=None)  # mocked connection

    # GIVEN driver is mocked to be connected
    JunosDriver.is_connected = True

    # GIVEN diff method will return changes
    junos_driver._driver.cu.diff.return_value = "fakediff"

    # GIVEN commit method will raise error
    junos_driver._driver.cu.commit.side_effect = RpcTimeoutError(
        dev=None, cmd=None, timeout=None
    )

    with pytest.raises(DriverCommitDisconnectError) as error:
        # WHEN calling replace config
        junos_driver.replace_config(
            config_filepath="/not/real/config.txt", format="set", commit_timer=10
        )

    # THEN expect error message
    assert str(error.value) == "host connection lost after commit"
