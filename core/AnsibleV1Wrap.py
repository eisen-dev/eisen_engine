# (c) 2015, Alice Ferrazzi <alice.ferrazzi@gmail.com>
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
import ansible
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import AnsibleV1Inv
import os
# we get the global celery worker from bin folder
from bin import celery_work

# return list of groups json formatted from ansible inventory
def GroupsList():
    """

    :rtype: object
    """
    groups = []
    a = inventory.Inventory()
    data = a.groups_list()
    for i in data:
        try:
            group = {
                'id': groups[-1]['id'] + 1,
                'group': str(i),
                'hosts': str(data[i]),
            }
        except:
            group = {
                'id': 1,
                'group': i,
                'hosts': data[i],
            }
        groups.append(group)
    return groups


# ???
def GroupsAvailability(hosts):
    pass


# search if host is present in the group list
# return the group name if found
def search(values, searchFor):
    founds = []
    for k in values:
        for v in values[k]:
            if searchFor in v:
                founds.append(k)
    return founds


# return list of host json formatted from ansible inventory
def HostsList():
    """

    :rtype: object
    """
    hosts = []
    a = inventory.Inventory()
    a= AnsibleV1Inv.get_inv()
    data = a.list_hosts()
    # data example
    # ['192.168.233.129', '192.168.233.131', '192.168.0.211']
    #data = a.list_hosts()
    # groups example
    # {'ungrouped': [],
    #  'all': ['192.168.233.129', '192.168.233.131', '192.168.0.211'],
    #  'vmware': ['192.168.233.129', '192.168.233.131'],
    #  'atom': ['192.168.0.211']}
    groups = a.groups_list()
    for i in range(len(data)):
        group = search(groups,data[i])
        try:
            host = {
                'id': hosts[-1]['id'] + 1,
                'host': str(data[i]),
                'groups': group
            }
        except:
            host = {
                'id': 1,
                'host': data[i],
                'groups': group
            }
        hosts.append(host)
    return hosts

# return list of host variable json mapping from ansible inventory
def HostVarsList(id):
    """

    :rtype: object
    """
    # init for contain the variable values
    vars = []
    # get the dynamic inventory
    a = AnsibleV1Inv.get_inv()
    # check for host
    data = a.list_hosts()
    host_vars = a.get_host(data[id]).get_variables()
    for i in host_vars:
        variable_key = i
        variable_value = host_vars[i]
        try:
            var = {
                'id': vars[-1]['id'] + 1,
                'host': str(data[id]),
                'variable_key': variable_key,
                'variable_value': variable_value
            }
        except:
            var = {
                'id': 1,
                'host': str(data[id]),
                'variable_key': variable_key,
                'variable_value': variable_value
            }
        vars.append(var)
    return vars

def GroupVarsList(group):
    """
    lists variables for group

    :rtype: object
    """
    vars = []
    a = inventory.Inventory()
    group_vars = a.get_group(group).get_variables()
    for i in range(len(vars)):
        try:
            host = {
                'id': len(vars)[-1]['id'] + 1,
                'group': str(group[i]),
                'groups': group
            }
        except:
            host = {
                'id': 1,
                'group': str(group[i]),
                'groups': group
            }
        vars.append(host)
    return vars

def TasksStart():
    """
    example init task

    :rtype: object
    """
    tasks = []
    for i in range(1):
        task = {
            'id': i+1,
            'hosts': 'localhost',
            'command' : '',
            'module' : 'ping',
        }
        tasks.append(task)
    return tasks

def RecipesStart():
    """
    example init task


    :rtype: object
    """
    recipes = []
    for i in range(1):
        task = {
            'id': i+1,
            'host': 'localhost',
            'file' : '/vagrant/vagrant/test_recipe.yml',
            'package' : 'git',
        }
        recipes.append(task)
    return recipes


@celery_work.task
def RunTask(hosts, commands, module, inv):
    """
    Running task with celery worker
    be sure the celery worker is running

    :param self:
    :param hosts:
    :param commands:
    :param module:
    :param inv:
    :return: async task object
    """
    runner = ansible.runner.Runner(module_name=module, module_args=commands,
                                   pattern=hosts, inventory=inv)
    get_facts = runner.run()
    return get_facts

def TasksList(hosts):
    """
    getting list of tasks

    :param hosts:
    :return:
    """
    pass

def RecepieList():
    """
    getting list of Recepies

    :return:
    """
    pass

def RunRecepie(inventory, playbook_file):
    """
    Run playbook

    :param hosts:
    :return:
    """
    # Boilerplace callbacks for stdout/stderr and log output
    utils.VERBOSITY = 0
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    pb = PlayBook(
        playbook=playbook_file,
        inventory=inventory,
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
    )

    results = pb.run()

    # Ensure on_stats callback is called
    # for callback modules
    playbook_cb.on_stats(pb.stats)

    return results