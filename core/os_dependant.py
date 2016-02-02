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
        result_string = dispatcher.PackageAction(module, pack['targetHost'], command, mod,
                                      pack['id'], pack)
        return result_string
    elif pack['targetOS'] == 'Gentoo':
        print 'loading module portage'

def os_remove_command(pack):
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