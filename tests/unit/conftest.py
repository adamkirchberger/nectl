import pytest
import pathlib

from nectl.config import Config


@pytest.fixture(scope="function")
def mock_datatree(tmp_path) -> pathlib.PosixPath:
    """
    Creates a datatree mock data and returns the path.

    Returns:
        pathlib.PosixPath: path to tmp datatree.
    """
    root = tmp_path / "data"
    root.mkdir()
    (root / "__init__.py").write_text("")

    (root / "glob" / "common").mkdir(parents=True)
    (root / "glob" / "roles").mkdir(parents=True)

    # Make fake customers
    for customer in ["acme", "hooli"]:
        c = root / "customers" / customer
        c.mkdir(parents=True)

        (c / "common").mkdir()
        (c / "roles").mkdir()
        (c / "sites").mkdir()

        # Make fake sites
        for site in ["london", "newyork"]:
            site = c / "sites" / site
            site.mkdir(parents=True)

            (site / "common").mkdir(parents=True)
            (site / "roles").mkdir(parents=True)

            hosts = site / "hosts"
            hosts.mkdir(parents=True)

            # Make fake hosts
            (hosts / "core0").mkdir()
            (hosts / "core1").mkdir()

    return root


@pytest.fixture(scope="function")
def mock_config(mock_datatree) -> Config:
    """
    Creates mock config with a datatree.

    Returns:
        Config: config settings.
    """
    datatree_path = mock_datatree

    return Config(
        kit_path=str(datatree_path.parent),
        config_path=str(datatree_path.parent) + "/config.yaml",
        datatree_lookup_paths=(
            "data.glob.common",
            "data.glob.roles.{role}",
            "data.customers.{customer}.common",
            "data.customers.{customer}.roles.{role}",
            "data.customers.{customer}.sites.{site}.common",
            "data.customers.{customer}.sites.{site}.roles.{role}",
            "data.customers.{customer}.sites.{site}.hosts.{hostname}",
        ),
        hosts_glob_pattern="customers/*/sites/*/hosts/*",
        hosts_hostname_regex=".*/sites/.*/hosts/(.*)$",
        hosts_site_regex=".*/sites/(.*)/hosts/.*",
        hosts_customer_regex=".*/customers/(.*)/sites/.*",
        blueprints_map={
            "fakeos:FakeOs": {
                "os_name_regex": "fakeos",
                "os_version_regex": "5.*",
            }
        },
    )
