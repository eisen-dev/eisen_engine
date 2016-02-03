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

