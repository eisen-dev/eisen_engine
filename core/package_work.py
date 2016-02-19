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

from os_dependant import os_install_command, os_remove_command, os_update_command
from threading import Thread

def package_get(pack):
    if pack['packageAction'] == 'install':
        print 'install package'
        result_string = Thread(target=os_install_command,args=[pack])
        result_string.start()
        return str(result_string)
    elif pack['packageAction'] == 'update':
        print 'update package'
        result_string = Thread(target=os_update_command,args=[pack])
        result_string.start()
        return str(result_string)
    elif pack['packageAction'] == 'delete':
        print 'deleting package'
        result_string = Thread(target=os_remove_command,args=[pack])
        result_string.start()
        return str(result_string)

