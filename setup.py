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

from distutils.core import setup

setup(
    name='eisen_engine',
    version='0.0.1',
    packages=['bin','core','resources'],
    scripts = ["bin/eisen_engine"],
    url='https://github.com/eisen-dev/eisen_engine',
    license='GPL2',
    classifiers=[
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    author='Alice Ferrazzi',
    author_email='alice.ferrazzi@gmail.com',
    description='eisen engine',
    requires=['Flask', 'sqlalchemy'],
    test_require=['nose'],
    test_suite='nose.collector',
    include_package_data=True,
    zip_safe=False
)
