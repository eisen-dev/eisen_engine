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

import dispatcher

def os_install_command(pack):
    """

    :param pack:
        pack['targetOS']
        pack['packageName']
        pack['packageVersion']
        pack['packageAction']
        pack['targetHost']
        pack['id']
    :return:
    """
    if pack['targetOS'] == 'Raspbian':
        pack['targetOS'] = 'Ubuntu'

    if pack['targetOS'] == 'Ubuntu':
        print 'loading module apt'

        mod = 'apt'
        state = 'present'
        module = dispatcher.use_module()

        command = 'name='+ pack['packageName']+' state='+state
        result_string = dispatcher.PackageAction(module, pack['targetHost'], command, mod,
                                      pack['id'], pack)
        return result_string
    elif pack['targetOS'] == 'Gentoo':
        print 'loading module portage'

def os_remove_command(pack):
    if pack['targetOS'] == 'Raspbian':
        pack['targetOS'] = 'Ubuntu'

    if pack['targetOS'] == 'Ubuntu':
        print 'loading module apt'
        mod = 'apt'
        state = 'absent'
        module = dispatcher.use_module()

        command = 'name='+ pack['packageName']+' state='+state
        result_string = dispatcher.PackageAction(module, pack['targetHost'], command, mod,
                                      pack['id'], pack)
        return result_string
    elif pack['targetOS'] == 'Gentoo':
        print 'loading module portage'

def os_update_command(pack):
    if pack['targetOS'] == 'Raspbian':
        pack['targetOS'] = 'Ubuntu'
    if pack['targetOS'] == 'Ubuntu':
        print 'loading module apt'
        mod = 'apt'
        state = 'present'
        module = dispatcher.use_module()

        command = 'name='+ pack['packageName']+' state='+state
        result_string = dispatcher.PackageAction(module, pack['targetHost'], command, mod,
                                      pack['id'], pack)
        return result_string
    elif pack['targetOS'] == 'Gentoo':
        print 'loading module portage'