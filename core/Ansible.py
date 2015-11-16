from ansible import inventory
import ansible
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils
import os


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
                'busy': 'false'
            }
        except:
            group = {
                'id': 1,
                'group': i,
                'hosts': data[i],
                'busy': 'false'
            }
        groups.append(group)
    return groups


def HostsList():
    """

    :rtype: object
    """
    hosts = []
    a = inventory.Inventory()
    data = a.list_hosts()
    print data
    for i in range(len(data)):
        try:
            host = {
                'id': hosts[-1]['id'] + 1,
                'host': str(data[i]),
            }
        except:
            host = {
                'id': 1,
                'host': data[i],
            }
        hosts.append(host)
    return hosts


def GroupsAvailability(hosts):
    pass


def RunTask(hosts, commands):
    #  __init__(self, host_list='/etc/ansible/hosts', module_path=None, module_name='command', module_args='', forks=5, timeout=10, pattern='*', remote_user='root', remote_pass=None, remote_port=None, private_key_file=None, background=0, basedir=None, setup_cache=None, vars_cache=None, transport='smart', conditional='True', callbacks=None, module_vars=None, play_vars=None, play_file_vars=None, role_vars=None, role_params=None, default_vars=None, extra_vars=None, is_playbook=False, inventory=None, subset=None, check=False, diff=False, environment=None, complex_args=None, error_on_undefined_vars=True, accelerate=False, accelerate_ipv6=False, accelerate_port=None, vault_pass=None, run_hosts=None, no_log=False, run_once=False, become=False, become_method='sudo', become_user=None, become_pass=None, become_exe=None)
    runner = ansible.runner.Runner(module_name='shell', module_args=commands, pattern='vmware', )
    get_facts = runner.run()
    print get_facts
    for i in get_facts:
        print i
        for x in get_facts[i]:
            for y in get_facts[i][x]:
                stdout = get_facts[i][x]['stdout']
    return stdout


def TasksList(hosts):
    pass


def RecepieList():
    pass


def RunRecepie(hosts, ):
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
