import glob
from genericpath import isfile
from os.path import dirname, basename
import Ansible


def ModulesList():
    modules = glob.glob(dirname(__file__) + "/*.py")

    # remove itself for not reimporting
    dispatcher = (glob.glob(dirname(__file__) + "/dispatcher.py"))
    modules.remove(dispatcher[0])

    __all__ = [basename(f)[:-3] for f in modules if isfile(f)]
    # mod = {}
    # for i in __all__:
    #    print i
    #    mod[i]=(__import__('core.'+ i))
    return __all__


# return usable mod
# def installed_mod():
# return(mod)

def use_module():
    # API chooser
    module = Ansible;
    return module


def HostsList(module):
    hosts = module.HostsList()
    return hosts


def GroupsList(module):
    groups = module.GroupsList()
    return groups


def TasksList(module):
    tasks = module.TasksStart()
    return tasks


def RunTask(module, hosts, command, mod):
    tasks = module.RunTask(hosts, command, mod)
    return tasks
