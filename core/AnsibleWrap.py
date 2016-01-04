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
import ansible
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import AnsibleInv
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
    # data example
    # ['192.168.233.129', '192.168.233.131', '192.168.0.211']
    data = a.list_hosts()
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

# return list of host variable json formatted from ansible inventory
def HostVarsList(id):
    """

    :rtype: object
    """
    print id
    vars = []
    a = AnsibleInv.get_inv()
    #a = inventory.Inventory()
    data = a.list_hosts()
    print data[id]
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

# return list of host variable json formatted from ansible inventory
def GroupVarsList(group):
    """

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

# make a init task and return as json format
def TasksStart():
    """

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


@celery_work.task
def RunTask(hosts, commands, module, inv):
    """
        __init__(self, host_list='/etc/ansible/hosts',
        module_path=None, module_name='command',
        module_args='',
        forks=5,
        timeout=10,
        pattern='*',
        remote_user='root',
        remote_pass=None,
        remote_port=None,
        private_key_file=None,
        background=0,
        basedir=None,
        setup_cache=None,
        vars_cache=None,
        transport='smart',
        conditional='True',
        callbacks=None,
        module_vars=None,
        play_vars=None,
        play_file_vars=None,
        role_vars=None,
        role_params=None,
        default_vars=None,
        extra_vars=None,
        is_playbook=False,
        inventory=None,
        subset=None,
        check=False,
        diff=False,
        environment=None,
        complex_args=None,
        error_on_undefined_vars=True,
        accelerate=False,
        accelerate_ipv6=False,
        accelerate_port=None,
        vault_pass=None,
        run_hosts=None,
        no_log=False,
        run_once=False,
        become=False, become_method='sudo',
        become_user=None, become_pass=None,
        become_exe=None)
    """
    runner = ansible.runner.Runner(module_name=module, module_args=commands,
                                   pattern=hosts, inventory=inv)
    get_facts = runner.run()
    return get_facts

# not used ???
def TasksList(hosts):
    pass

# not used ???
def RecepieList():
    pass

# run playbook
def RunRecepie(hosts):
    # Boilerplace callbacks for stdout/stderr and log output
    utils.VERBOSITY = 0
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    stats = callbacks.AggregateStats()
    runner_cb = callbacks.PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    pb = PlayBook(
        playbook='/path/to/main/playbook.yml',
        host_list=hosts.name,  # Our hosts, the rendered inventory file
        remote_user='some_user',
        callbacks=playbook_cb,
        runner_callbacks=runner_cb,
        stats=stats,
        private_key_file='/path/to/key.pem'
    )

    results = pb.run()
    os.remove(hosts.name)

    # Ensure on_stats callback is called
    # for callback modules
    playbook_cb.on_stats(pb.stats)

    return results