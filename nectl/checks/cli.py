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

import sys
import click

from ..nectl import Nectl
from ..logging import logging_opts


@click.group(help="Validation commands.")
@logging_opts
def checks():
    """
    Checks CLI group.
    """


@checks.command(name="list", help="List checks.")
@click.option("-k", "--pytest-expression", help="Only run checks matching expression.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.pass_context
@logging_opts
def list_cmd(
    ctx,
    pytest_expression: str,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
):
    """
    Use this command to list all configured checks.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
        results = nectl.list_checks(
            hosts=sorted(
                hosts.values(),
                key=lambda host: (host.customer, host.site, host.id),
            ),
            pytest_expression=pytest_expression,
        )

        print(f"{len(results)} checks found.")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


@checks.command(name="run", help="Run checks.")
@click.option("-k", "--pytest-expression", help="Only run checks matching expression.")
@click.option("-h", "--hostname", help="Filter by hostname.")
@click.option("-c", "--customer", help="Filter by customer.")
@click.option("-s", "--site", help="Filter by site.")
@click.option("-r", "--role", help="Filter by role.")
@click.option("-d", "--deployment-group", help="Filter by deployment group.")
@click.pass_context
@logging_opts
def run_cmd(
    ctx,
    pytest_expression: str,
    hostname: str,
    customer: str,
    site: str,
    role: str,
    deployment_group: str,
):
    """
    Use this command to run checks.
    """
    try:
        nectl = Nectl(settings=ctx.obj["settings"])
        hosts = nectl.get_hosts(
            hostname=hostname,
            customer=customer,
            site=site,
            role=role,
            deployment_group=deployment_group,
        )
        results = nectl.run_checks(
            hosts=sorted(
                hosts.values(),
                key=lambda host: (host.customer, host.site, host.id),
            ),
            pytest_expression=pytest_expression,
        )

        print(f"report written to: {results['report']}")

        if results["failed"]:
            sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
