from ansible import inventory

def HostsList():
    """

    :rtype: object
    """
    hosts = []
    a = inventory.Inventory()
    data = a.groups_list()

    for i in data:
        try:
            host = {
                'id': hosts[-1]['id'] + 1,
                'group' : str(i),
                'hosts': str(data[i]),
                'jobs': u'ping',
                'busy': 'false'
            }
        except:
            host = {
                     'id': 1,
                     'group': i,
                     'hosts': data[i],
                     'jobs': u'ping',
                     'busy': 'false'
                 }
        hosts.append(host)
    return hosts

def HostsAvailability(hosts):
    pass

def HostsCommands(hosts,commands):
    pass

def TasksList(hosts):
    pass

def StartTasks(module_name,module_args,pattern):
    pass

def StopTasks(tasks,hosts):
    pass
