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
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, bindparam, select
from AnsibleWrap import RunTask
import AnsibleInv
import traceback

engine = create_engine('mysql://root:password@192.168.33.15:3306/eisen',
                       echo=True)

metadata = MetaData(bind=engine)

def package_update(command):
    a= AnsibleInv.get_inv()
    host = a.list_hosts()
    print host
    target_host = Table('target_host', metadata, autoload=True, autoload_with=engine)
    s = select([target_host])
    result = engine.execute(s)
    print result
    for i in host:
        for row in result:
            if row['ipaddress'] == i:
                os = row['os']
                print os
                command_installed = repository_installed(os)
                command_all = repository_all(os)
                try:
                    get_installed_package(host, command_installed, os)
                except Exception as e:
                    print(traceback.format_exc())
                try:
                    get_all_package(host, command_all, os)
                except Exception as e:
                    print(traceback.format_exc())

def repository_installed(os):
    if os == 'Ubuntu':
        command = "dpkg -l | awk 'NR>5{print $0}'"
    elif os == 'Gentoo':
        command = "equery --no-pipe --quiet list '*' -F '$category $name $fullversion'"
    else:
        command = None
    return command

def repository_all(os):
    if os == 'Ubuntu':
        command = "dpkg -l \"*\" | grep -v '^ii'| awk 'NR>5{print $0}'"
    elif os == 'Gentoo':
        command = "equery --no-pipe --quiet list -po '*' -F '$category $name " \
                  "$fullversion'"
    else:
        command = None
    return command

def get_installed_package(target_host_ip, command, target_host_os):
    a= AnsibleInv.get_inv()
    packages = RunTask(target_host_ip, command,"shell",a)
    target_host_ip = target_host_ip[0]
    if target_host_os == 'Ubuntu':
        dpkg_lines = packages['contacted'][target_host_ip]['stdout']
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
            update_installed_package_db(stripe[1],stripe[2],summary,target_host_ip,target_host_os)
    elif target_host_os == 'Gentoo':
        package_line = packages['contacted'][target_host_ip]['stdout']
        package_list = package_line.split('\n')
        for package in package_list:
            category_name_version = package.split(' ')
            package_category = category_name_version[0]
            package_name = category_name_version[1]
            packge_version = category_name_version[2]
            summary = 'none'
            update_repository_package_db(package_category+'/'+package_name,packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)
    else:
        print 'failed'

def get_all_package(target_host_ip, command, target_host_os):
    a= AnsibleInv.get_inv()
    packages = RunTask(target_host_ip, command,"shell",a)
    target_host_ip = target_host_ip[0]
    if target_host_os == 'Ubuntu':
        dpkg_lines = packages['contacted'][target_host_ip]['stdout']
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
            update_repository_package_db(stripe[1],stripe[2],summary,target_host_ip,
                                 target_host_os)
    elif target_host_os == 'Gentoo':
        package_line = packages['contacted'][target_host_ip]['stdout']
        package_list = package_line.split('\n')
        for package in package_list:
            category_name_version = package.split(' ')
            package_category = category_name_version[0]
            package_name = category_name_version[1]
            packge_version = category_name_version[2]
            summary = 'none'
            update_repository_package_db(package_category+'/'+package_name,packge_version,
                                         summary,
                                         target_host_ip,
                                         target_host_os)

    else:
        print 'failed'

def update_installed_package_db(package_name,package_version,package_summary,
                                target_host_ip, target_host_os):
    installed_package = Table('installed_package', metadata, autoload=True,
                        autoload_with=engine)
    stmt = installed_package.insert()
    result = engine.execute(stmt, installed_pack_name=package_name,
    installed_pack_version=package_version,
                            installed_pack_summary=package_summary,
                            target_host=target_host_ip, pack_sys_id=1)
    pass

def update_repository_package_db(package_name,package_version,package_summary,
                                target_host_ip, target_host_os):
    repository_package = Table('pack_info', metadata, autoload=True,
                        autoload_with=engine)
    stmt = repository_package.insert()
    result = engine.execute(
        stmt,
        pack_name=package_name,
        pack_version=package_version,
        pack_summary=package_summary,
        target_host=target_host_ip,
        pack_sys_id=1
    )
    pass

def get_os():
    a= AnsibleInv.get_inv()
    host = a.list_hosts()
    for i in host:
        version = RunTask(host,"bash -c 'cat /etc/*{release,version}'","shell",a)
        print version
        print str(i) +':'+ str(host)
        print "failed"
        stdout = version['contacted'][str(i)]['stdout']
        print stdout
        check_os(stdout,i)


def check_os(stdout,i):
    if (stdout.find('Ubuntu') is not -1):
        submit_os_db('Ubuntu',i)
        print('Ubuntu',i)
    elif (stdout.find('Gentoo') is not -1):
        submit_os_db('Gentoo', i)
        print('Gentoo',i)
    else:
        submit_os_db('Unknown', i)
        print('Unknown',i)

def submit_os_db(os, host):
    target_host = Table('target_host', metadata, autoload=True, autoload_with=engine)
    stmt = (target_host.update().
        where(target_host.c.ipaddress == bindparam('host')).
        values(os=bindparam('os'))
        )
    result=engine.execute(stmt, [{"host": host, "os": os}])