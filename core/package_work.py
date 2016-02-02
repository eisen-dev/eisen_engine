from os_dependant import os_install_command, os_remove_command, os_update_command

def package_get(pack):
    if pack['packageAction'] == 'install':
        print 'install package'
        result_string = os_install_command(pack)
        return result_string
    elif pack['packageAction'] == 'update':
        print 'update package'
        result_string = os_update_command(pack)
        return result_string
    elif pack['packageAction'] == 'delete':
        print 'deleting package'
        result_string = os_remove_command(pack)
        return result_string

