# (c) 2012-2015, Alice Ferrazzi <alice.ferrazzi@gmail.com>
#
# This file is part of Eisen
#
# Eisen is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Eisen is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Eisen.  If not, see <http://www.gnu.org/licenses/>.

from ansible import inventory
from Ansible import search
import ansible

inv = inventory.Inventory()

def set_host(name, port):
    inv_host = inventory.host.Host(name = name, port = port)
    return inv_host

def set_host_variable(variable_name,variable,inv_host):
    inv_host.set_variable(variable_name, variable)
    return inv_host

def set_group(name):
    a = inventory.Inventory()
    groups = a.groups_list()
    group_exist = False
    for i in groups:
        if name in i:
            group_exist=True
    if group_exist is True:
        inv_group = inventory.get_group(name)
    else:
        inv_group = inventory.group.Group(name = name)
    return inv_group

def set_group_variable(variable_name,variable,inv_host):
    inv_host.set_variable(variable_name, variable)
    return inv_host

def set_group_host(inv_group, inv_host):
    inv_group.add_host(inv_host)
    return inv_group

def set_inv(inv_group):
    global inv
    inv.add_group(inv_group)
    return inv

def get_inv():
    global inv
    return inv