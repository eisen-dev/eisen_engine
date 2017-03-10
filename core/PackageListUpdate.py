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
from threading import Thread

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
    else:
        print 'failed'


def get_all_package(target_host_ip, command, target_host_os):
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
    else:
        print 'failed'


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
        except Exception, error:
            print ("couldn't connect to"+ i )


def add_description(os, package, language='ja_JP'):
    print (os, package, language)
    command_package_description_start = "apt-cache show "
    command_package_description_end =" | awk '$1 == " \
                                      "\"Description-en:\" { print substr($0, " \
                                      "17) }' |head -n 1"


def package_summary(language, package_name, summary, os):
    summary = 'uknown'

    return summary