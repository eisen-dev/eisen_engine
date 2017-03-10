# coding=utf-8
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
from sqlalchemy import *
from AnsibleV1Wrap import RunTask
import AnsibleV1Inv
import traceback
from mysql_config import start_engine
from threading import Thread

engine , metadata = start_engine()


def package_update(targetHost, os, command):
    if os == 'Raspbian':
        os = 'Ubuntu'
    print (
        '\n------------------------------------' + targetHost
        + '--' + os + '--' +command+ '--------------------------------\n')
    command_installed = repository_installed(os)
    command_all = repository_all(os)
    if command == 'installed':
        try:
            print 'get installed package'
            thr = Thread(target=get_installed_package, args=[targetHost, command_installed, os])
            thr.start()
        except Exception as e:
            print(traceback.format_exc())
    if command == 'respository':
        try:
            thr1 = Thread(target=get_all_package, args=[targetHost, command_all, os])
            thr1.start()
        except Exception as e:
            print(traceback.format_exc())
    if command == 'all':
        try:
            thr = Thread(target=get_installed_package, args=[targetHost, command_installed, os])
            thr.start()
        except Exception as e:
            print(traceback.format_exc())
        try:
            thr1 = Thread(target=get_all_package, args=[targetHost, command_all, os])
            thr1.start()
        except Exception as e:
            print(traceback.format_exc())


def repository_installed(os):
    print os
    if os == 'Ubuntu' or os == 'Raspbian':
        command = "dpkg -l | awk 'NR>5{print $0}'"
    elif os == 'Gentoo':
        command = "equery --no-pipe --quiet list '*' -F '$category $name $fullversion'"
    elif os == 'CentOS':
        command = "yum list installed | sed '1,2d'"
    else:
        print 'not supported yet'
        command = None
    return command


def repository_all(os):
    print os
    if os == 'Ubuntu' or os == 'Raspbian':
        command = "apt-cache search ."
    elif os == 'Gentoo':
        command = "equery --no-pipe --quiet list -po '*' -F '$category $name " \
                  "$fullversion'"
    elif os == 'CentOS':
        command = "yum list | sed '1,2d' "
    else:
        print 'not supported yet'
        command = None
    return command


def get_installed_package(target_host_ip, command, target_host_os):
    delete_user_machine_packages(target_host_ip)
    a= AnsibleV1Inv.get_inv()
    packages = RunTask(target_host_ip, command,"shell",a)
    if target_host_os == 'Ubuntu':
        try:
            dpkg_lines = packages['contacted'][target_host_ip]['stdout']
        except Exception, error:
            print error
            pass
        dpkg_lines = dpkg_lines.split('\n')
        # dividing dpkg output and dividing the package summary from the other
        # information
        for dpkg_line in dpkg_lines:
            dpkg_line = dpkg_line.split(' ')
            stripe = []
            summary = []
            i = 0
            for point in dpkg_line:
                if point != '' and i<3:
                    stripe.append(point)
                    i+=1
                elif point !='' and i>=3:
                    summary.append(point)
                    i+=1
            s = ' '
            summary = s.join(summary)
            #language = 'jp'
            #summary = package_summary(language, stripe[1], summary, target_host_os)
            try:
                update_installed_package_db(stripe[1], (stripe[2]), summary,
                                            target_host_ip,target_host_os)
            except Exception, error:
                print error
                pass
    elif target_host_os == 'Gentoo':
        try:
            package_line = packages['contacted'][target_host_ip]['stdout']
        except Exception, error:
            print error
            pass
        package_list = package_line.split('\n')
        print package_list
        for package in package_list:
            category_name_version = package.split(' ')
            package_category = category_name_version[0]
            package_name = category_name_version[1]
            packge_version = category_name_version[2]
            summary = 'none'
            try:
                update_installed_package_db(package_category+'/'+package_name,packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)
            except Exception, error:
                print error
    elif target_host_os == 'CentOS':
        try:
            package_line = packages['contacted'][target_host_ip]['stdout']
        except:
            print 'ssh problems'
            return 'ssh problems'
        package_list = package_line.split('\n')
        print package_list
        for package in package_list:
            category_name_version = package.split(' ')
            category_name_version = filter(None, category_name_version)
            print category_name_version
            if len(category_name_version) == 1:
                package_name = category_name_version[0]
                packge_version = 'none'
            else:
                package_name = category_name_version[0]
                packge_version = category_name_version[1]
            summary = 'none'
            try:
                update_installed_package_db(package_name,packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)
            except Exception, error:
                print error
    else:
        print 'failed'


def get_all_package(target_host_ip, command, target_host_os):
    delete_repository_package_db(target_host_ip)
    a= AnsibleV1Inv.get_inv()
    packages = RunTask(target_host_ip, command,"shell",a)
    if target_host_os == 'Ubuntu':
        try:
            dpkg_lines = packages['contacted'][target_host_ip]['stdout']
            dpkg_lines = dpkg_lines.split('\n')
            # dividing dpkg output and dividing the package summary from the other
            # information
            for dpkg_line in dpkg_lines:
                package_name_version_summary_type = dpkg_line.split(' - ')
                package_name = package_name_version_summary_type[0]
                package_version = u'-'
                package_summary = package_name_version_summary_type[1]
                try:
                    update_repository_package_db(package_name,
                                                 package_version,
                                                 package_summary,
                                                 target_host_ip,
                                     target_host_os)
                except Exception, error:
                    print error
        except Exception, error:
            print error
            pass
    elif target_host_os == 'Gentoo':
        package_line = packages['contacted'][target_host_ip]['stdout']
        package_list = package_line.split('\n')
        for package in package_list:
            category_name_version = package.split(' ')
            package_category = category_name_version[0]
            package_name = category_name_version[1]
            packge_version = category_name_version[2]
            summary = 'none'
            try:
                update_repository_package_db(package_category+'/'+package_name,
                                              packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)
            except Exception, error:
                print error
    elif target_host_os == 'CentOS':
        try:
            package_line = packages['contacted'][target_host_ip]['stdout']
        except:
            print 'ssh problems'
            return 'ssh problems'
        package_list = package_line.split('\n')
        print package_list
        for package in package_list:
            category_name_version = package.split(' ')
            category_name_version = filter(None, category_name_version)
            print category_name_version
            if len(category_name_version) == 1:
                package_name = category_name_version[0]
                packge_version = 'none'
            else:
                package_name = category_name_version[0]
                packge_version = category_name_version[1]
            summary = 'none'
            try:
                update_installed_package_db(package_name,packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)
            except Exception, error:
                print error
    else:
        print 'failed'


def delete_user_machine_packages(target_host_ip):
    print '======================================delete: ' \
          ''+target_host_ip+'=================================================='
    connection = engine.connect()
    installed_package = Table('installed_package', metadata, autoload=True,
                    autoload_with=engine)
    try:
        stmt = installed_package.delete().where(
            installed_package.c.target_host==target_host_ip)
        connection.execute(stmt)
        connection.close()
    except Exception, error:
        connection.close()
        print (error)
        pass


def update_installed_package_db(package_name,package_version,package_summary,
                                target_host_ip, target_host_os):
    connection = engine.connect()
    installed_package = Table('installed_package', metadata, autoload=True,
                    autoload_with=engine)
    try:
        stmt = installed_package.insert()
        connection.execute(
            stmt,
            installed_pack_name=package_name,
            installed_pack_version=package_version,
            installed_pack_summary=package_summary,
            target_host=target_host_ip,
            pack_sys_id=1
        )
        connection.close()
    except Exception, error:
        connection.close()
        print (error)


def update_repository_package_db(package_name,package_version,package_summary,
                                target_host_ip, target_host_os):
    connection = engine.connect()
    try:
        repository_package = Table('pack_info', metadata, autoload=True,
                            autoload_with=engine)
        stmt = repository_package.insert()
        connection.execute(
            stmt,
            pack_name=package_name,
            pack_version=package_version,
            pack_summary=package_summary,
            target_host=target_host_ip,
            pack_sys_id=1
        )
        connection.close()
    except Exception, error:
        connection.close()
        print (error)


def delete_repository_package_db(target_host_ip):
    print '======================================delete: ' \
          ''+target_host_ip+'=================================================='
    connection = engine.connect()
    try:
        repository_package = Table('pack_info', metadata, autoload=True,
                            autoload_with=engine)
        stmt = repository_package.delete()
        connection.execute(
            stmt,
            repository_package.c.target_host==target_host_ip,
            pack_sys_id=1
        ).execution_options(autocommit=True)
        connection.close()
    except Exception, error:
        connection.close()
        print (error)
        pass


def get_os():
    a= AnsibleV1Inv.get_inv()
    host = a.list_hosts()
    for i in host:
        version = RunTask(host,"bash -c 'cat /etc/*{release,version}'","shell",a)
        print version
        print ('connecting to: ' + str(i) +':'+ str(host))
        try:
            stdout = version['contacted'][str(i)]['stdout']
            print stdout
            check_os(stdout,i)
        except Exception, error:
            print ("couldn't connect to"+ i )
            offline_target_os(i)


def add_description(os, package, language='ja_JP'):
    print (os, package, language)
    command_package_description_start = "apt-cache show "
    command_package_description_end =" | awk '$1 == " \
                                      "\"Description-en:\" { print substr($0, " \
                                      "17) }' |head -n 1"


def package_summary(language, package_name, summary, os):
    summary = 'uknown'

    return summary


def check_os(stdout,i):
    if (stdout.find('Ubuntu') is not -1):
        submit_os_db('Ubuntu',i)
        print('Ubuntu',i)
    elif (stdout.find('Gentoo') is not -1):
        submit_os_db('Gentoo', i)
        print('Gentoo',i)
    elif (stdout.find('CentOS') is not -1):
        submit_os_db('CentOS', i)
        print('CentOS',i)
    elif (stdout.find('Raspbian') is not -1):
        submit_os_db('Raspbian', i)
        print('Raspbian',i)
    else:
        submit_os_db('Unknown', i)
        print('Unknown',i)


def submit_os_db(os, host):
    target_host = Table('target_host', metadata, autoload=True, autoload_with=engine)
    stmt = (target_host.update().
        where(target_host.c.ipaddress == bindparam('host')).
        values(os=bindparam('os'),status_id=bindparam('status_id'))
        )
    result=engine.execute(stmt, [{"host": host, "os": os, "status_id" : "online"}])


def offline_target_os(host):
    target_host = Table('target_host', metadata, autoload=True, autoload_with=engine)
    stmt = (target_host.update().
        where(target_host.c.ipaddress == bindparam('host')).
        values(status_id=bindparam('status_id'))
        )
    result=engine.execute(stmt, [{"host": host, "status_id": "offline"}])