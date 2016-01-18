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
import glob
from genericpath import isfile
from os.path import dirname, basename
import AnsibleWrap
import core.AnsibleInv as ans_inv
import ansible
# using global tasks_result dictionary for keeping the async result
from core import tasks_result

def ModulesList():
    """
    Get list of all available module:
    ansible

    :return: list
    """
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

#TODO make the Agent  Module be choosen using API
#update and only 1 agent module is needed
def AgentInfo(module=None):
    """

    :rtype: object
    """
    agents = []
    agent = {
        'id': 1,
        'module': 'Ansible',
        'version' : ansible.__version__,
    }
    agents.append(agent)
    return agents

def PackageUpdate(module=None):
    """

    :rtype: object
    """
    packs = []
    pack = {
        'id': 1,
        'command': 'Started',
    }
    packs.append(pack)
    return packs

def use_module():
    # API chooser
    module = AnsibleWrap
    return module

def HostsList(module):
    hosts = module.HostsList()
    return hosts

def HostVarsList(module, id):
    vars = module.HostVarsList(id)
    return vars

def GroupVarsList(module, group):
    vars = module.GroupVarsList(group)
    return vars

def GroupsList(module):
    groups = module.GroupsList()
    return groups


def TasksList(module):
    """
    making the init example task
    :param module:
    :return: Json
    """
    #TODO (alice): maybe default task is a better name?
    tasks = module.TasksStart()
    return tasks

def RunTask(module, hosts, command, mod, id):
    """
    Run Task asyncronously
    :param module:
    :param hosts:
    :param command:
    :param mod:
    :param id:
    :return: String
    """
    #retriving dynamic inventory from AnsibleInv
    inv = ans_inv.get_inv()
    #Starting async task and return
    tasks_result[id] = module.RunTask.delay(hosts, command, mod, inv)
    return "task started"

def ResultTask(id):
    """

    :param id:
    :return: String
    """
    # Cheking async task result
    if tasks_result[id].ready() is False:
        return "not ready yet!"
    else:
        return tasks_result[id].get()