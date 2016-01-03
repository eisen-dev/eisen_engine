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
    tasks = module.TasksStart()
    return tasks


def RunTask(module, hosts, command, mod):
    inv = ans_inv.get_inv()
    tasks = module.RunTask(hosts, command, mod, inv)
    return tasks