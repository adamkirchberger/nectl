# Copyright (C) 2022 Adam Kirchberger
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


def version(os_version):
    print(f'set version "{os_version}"')


def hostname(id):
    # Use 'id' fact which generates a unique name for host
    # Returns: {hostname}.{site}
    print(f"set system host-name {id}")


def root_user_config(root_password):
    print(f'set system root-authentication encrypted-password "{root_password}"')


def admin_user_config():
    print("set system login user admin uid 2000")
    print("set system login user admin class super-user")
    # admin@123
    print(
        'set system login user admin authentication encrypted-password "$6$Y5lVRa.c$8IgiORgdqDvyTNyE1K6PJtwr5UfVu5zOQuVS.mPA4fWBJlPfONCRBgJzrU7IAm0LoGYeFmhquQujDus.uM0C01"'
    )


def default_syslog():
    print("set system syslog user * any emergency")
    print("set system syslog file messages any any")
    print("set system syslog file messages authorization info")
    print("set system syslog file interactive-commands interactive-commands any")


def system_services_config():
    print("set system services ssh root-login allow")
    print("set system services netconf ssh")


def configure_login_message(login_message="Be careful when making changes."):
    print(f'set system login announcement "\\n\\n{login_message}\\n\\n"')
