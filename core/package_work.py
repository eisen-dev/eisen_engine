from os_dependant import os_install_command

def package_get(pack):
    if pack['packageAction'] == 'install':
        print 'install package'
        os_install_command(pack)
    elif pack['packageAction'] == 'update':
        print 'update package'
    elif pack['packageAction'] == 'delete':
        print 'deleting package'

