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

    if pack['targetOS'] == 'Ubuntu':
        print 'loading module apt'

        mod = 'apt'
        state = 'present'
        module = dispatcher.use_module()

        command = 'name='+ pack['packageName']+' state='+state
        dispatcher.PackageAction(module, pack['targetHost'], command, mod,
                                      pack['id'], pack)
    elif pack['targetOS'] == 'Gentoo':
        print 'loading module portage'

def os_remove_command(distribution):
    if distribution == 'Ubuntu':
        print 'loading module apt'
        module = 'apt'
        state = 'absent'
        return module, state
    elif distribution == 'Gentoo':
        print 'loading module portage'

def os_update_command(distribution):
    if distribution == 'Ubuntu':
        print 'loading module apt'
        module = 'apt'
        state = 'present'
        return module, state
    elif distribution == 'Gentoo':
        print 'loading module portage'