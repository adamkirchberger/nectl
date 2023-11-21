# Copyright (C) 2023 Adam Kirchberger
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

import os
import time
from typing import Optional, List, Dict
import pytest

from .logging import get_logger
from .settings import load_settings, Settings
from .exceptions import DriverError, ChecksError
from .datatree.hosts import Host
from .datatree.hosts import get_filtered_hosts
from .configs.render import render_hosts
from .configs.utils import write_configs_to_dir
from .configs.drivers import run_driver_method_on_hosts
from .checks.plugins import ChecksPlugin

logger = get_logger()


class Nectl:
    def __init__(
        self, kit_filepath: Optional[str] = None, settings: Optional[Settings] = None
    ) -> None:
        """
        Network control framework for network automation and orchestration.
        """
        self.settings = settings if settings else load_settings(filepath=kit_filepath)

    def get_hosts(
        self,
        hostname: Optional[str] = None,
        customer: Optional[str] = None,
        site: Optional[str] = None,
        role: Optional[str] = None,
        deployment_group: Optional[str] = None,
    ) -> Dict[str, Host]:
        """
        Get hosts from datatree that match supplied filter parameters.

        Args:
            hostname (str): optional hostname to filter by.
            customer (str): optional customer to filter by.
            site (str): optional site to filter by.
            role (str): optional role to filter by.
            deployment_group (str): optional deployment_group to filter by.

        Returns:
            Dict[str, Host]: discovered host instances mapped by host ID.

        Raises:
            DiscoveryError: when an error has been encountered during data tree discovery.
        """
        return get_filtered_hosts(
            settings=self.settings,
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )

    def render_configs(self, hosts: List[Host]) -> str:
        """
        Render configs for hosts and write them to the staged configs directory.

        Args:
            hosts (List[Hosts]): hosts to render templates for.

        Returns:
            str: configs output directory.

        Raises:
            RenderError: when render of hosts has encountered an error.
        """
        configs = render_hosts(settings=self.settings, hosts=hosts)
        output_dir = f"{self.settings.kit_path}/{self.settings.staged_configs_dir}"
        write_configs_to_dir(
            configs=configs,
            output_dir=output_dir,
            extension=self.settings.configs_file_extension,
        )
        return output_dir

    def diff_configs(
        self,
        hosts: List[Host],
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssh_private_key_file: Optional[str] = None,
    ) -> str:
        """
        Compare rendered config and active configurations on hosts.

        Args:
            hosts (List[Hosts]): hosts to generate diff for.
            username (str): optional host username, else reads fact from datatree.
            password (str): optional host username, else reads fact from datatree.
            ssh_private_key_file (str): optional ssh private key file.

        Returns:
            str: diffs output directory.

        Raises:
            DriverError: when an error has been encountered by the host driver.
        """
        total_errors, host_outputs = run_driver_method_on_hosts(
            settings=self.settings,
            hosts=hosts,
            method_name="compare_config",
            description="comparing host configurations",
            username=username,
            password=password,
            ssh_private_key_file=ssh_private_key_file,
        )

        output_dir = f"{self.settings.kit_path}/{self.settings.config_diffs_dir}"
        write_configs_to_dir(
            configs=host_outputs,
            output_dir=output_dir,
            extension="diff." + self.settings.configs_file_extension,
        )

        if total_errors:
            raise DriverError(f"{total_errors} errors encountered, see logs above.")

        return output_dir

    def apply_configs(
        self,
        hosts: List[Host],
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssh_private_key_file: Optional[str] = None,
    ) -> str:
        """
        Apply rendered config onto hosts.

        Args:
            hosts (List[Hosts]): hosts to generate diff for.
            username (str): optional host username, else reads fact from datatree.
            password (str): optional host username, else reads fact from datatree.
            ssh_private_key_file (str): optional ssh private key file.

        Returns:
            str: diffs output directory.

        Raises:
            DriverError: when an error has been encountered by the host driver.
        """
        total_errors, host_outputs = run_driver_method_on_hosts(
            settings=self.settings,
            hosts=hosts,
            method_name="apply_config",
            description="applying host configurations",
            username=username,
            password=password,
            ssh_private_key_file=ssh_private_key_file,
        )

        output_dir = f"{self.settings.kit_path}/{self.settings.config_diffs_dir}"
        write_configs_to_dir(
            configs=host_outputs,
            output_dir=output_dir,
            extension="diff." + self.settings.configs_file_extension,
        )

        if total_errors:
            raise DriverError(f"{total_errors} errors encountered, see logs above.")

        return output_dir

    def get_configs(
        self,
        hosts: List[Host],
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssh_private_key_file: Optional[str] = None,
    ) -> str:
        """
        Get active configs from hosts.

        Args:
            hosts (List[Hosts]): hosts to generate diff for.
            username (str): optional host username, else reads fact from datatree.
            password (str): optional host username, else reads fact from datatree.
            ssh_private_key_file (str): optional ssh private key file.

        Returns:
            str: active configs output directory.

        Raises:
            DriverError: when an error has been encountered by the host driver.
        """
        total_errors, host_outputs = run_driver_method_on_hosts(
            settings=self.settings,
            hosts=hosts,
            method_name="get_config",
            description="getting host configurations",
            username=username,
            password=password,
            ssh_private_key_file=ssh_private_key_file,
        )

        output_dir = f"{self.settings.kit_path}/{self.settings.active_configs_dir}"
        write_configs_to_dir(
            configs=host_outputs,
            output_dir=output_dir,
            extension=self.settings.configs_file_extension,
        )

        if total_errors:
            raise DriverError(f"{total_errors} errors encountered, see logs above.")

        return output_dir

    def run_checks(
        self,
        hosts: List[Host],
        pytest_expression: str = "",
    ) -> dict:
        """
        Run checks on hosts.

        Args:
            hosts (List[Hosts]): hosts to generate diff for.
            pytest_expression (str): optional pytest match expression.

        Returns:
            dict: {"passed": int, "failed": int, "report": str}

        Raises:
            ChecksError: when an error has been encountered during pytest run.
        """
        ts_start = time.perf_counter()
        logger.debug("starting checks run")

        # Register plugin with hosts
        checks_plugin = ChecksPlugin(hosts=hosts)

        report_filepath = os.path.join(
            self.settings.kit_path, self.settings.checks_report_filename
        )

        pytest_args = [
            "-c=''",
            "-vv",
            "--tb=short",
            "-p",
            "no:warnings",
            f"-o=python_files={self.settings.checks_prefix}_*.py",
            f"-o=python_classes={self.settings.checks_prefix.capitalize()}",
            f"-o=python_functions={self.settings.checks_prefix}_*",
            f"--junitxml={report_filepath}",
        ]

        if pytest_expression:
            pytest_args.extend(
                [
                    "-k",
                    pytest_expression,
                ]
            )

        # Run pytest using checks plugin
        rc = pytest.main(
            (
                pytest_args
                + [os.path.join(self.settings.kit_path, self.settings.checks_dirname)]
            ),
            plugins=[checks_plugin],
        )

        dur = f"{time.perf_counter()-ts_start:0.4f}"
        logger.info(
            "finished checks run "
            f"pass={checks_plugin.passed} fail={checks_plugin.failed} rc={rc} ({dur}s)"
        )

        if rc not in [0, 1]:
            raise ChecksError(
                "pytest encountered an error, ensure check files are valid!"
            )

        return {
            "passed": checks_plugin.passed,
            "failed": checks_plugin.failed,
            "report": report_filepath,
        }

    def list_checks(
        self,
        hosts: List[Host],
        pytest_expression: str = "",
    ) -> List[str]:
        """
        List checks that will run on hosts.

        Args:
            hosts (List[Hosts]): hosts to generate diff for.
            pytest_expression (str): optional pytest match expression.

        Returns:
            List[str]: list of check names that would run.

        Raises:
            ChecksError: when an error has been encountered during pytest run.
        """
        ts_start = time.perf_counter()
        logger.debug("starting checks list")

        # Register plugin with hosts
        checks_plugin = ChecksPlugin(hosts=hosts)

        pytest_args = [
            "-c=''",
            "-p",
            "no:warnings",
            "--collect-only",
            f"-o=python_files={self.settings.checks_prefix}_*.py",
            f"-o=python_classes={self.settings.checks_prefix.capitalize()}",
            f"-o=python_functions={self.settings.checks_prefix}_*",
        ]

        if pytest_expression:
            pytest_args.extend(
                [
                    "-k",
                    pytest_expression,
                ]
            )

        # Run pytest using checks plugin
        rc = pytest.main(
            (
                pytest_args
                + [os.path.join(self.settings.kit_path, self.settings.checks_dirname)]
            ),
            plugins=[checks_plugin],
        )

        dur = f"{time.perf_counter()-ts_start:0.4f}"
        logger.info(
            "finished checks list "
            f"selected={len(checks_plugin.tests_selected)} "
            f"total={len(checks_plugin.tests)} rc={rc} ({dur}s)"
        )

        if rc not in [0, 1]:
            raise ChecksError(
                "pytest encountered an error, ensure check files are valid!"
            )

        return checks_plugin.tests_selected
