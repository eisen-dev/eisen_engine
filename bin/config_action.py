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

import os
import shutil
import configparser


def write():
    config = configparser.ConfigParser()

    config.add_section('REST')
    config.add_section('SSL')
    config.add_section('SQLALCHEMY')
    config.add_section('CELERY')

    config['REST']['SECRET_KEY'] = "SECRET_KEY"
    config['SSL']['SSL_DISABLE'] = "False"
    config['SQLALCHEMY']['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = "True"
    config['SQLALCHEMY']['SQLALCHEMY_RECORD_QUERIES'] = "True"
    config['CELERY']['CELERY_BROKER_URL'] = 'amqp://guest@localhost//'
    config['CELERY']['CELERY_RESULT_BACKEND'] = 'amqp'

    with open(".eisen_engine.conf", 'w') as f:
        config.write(f)


def read():
    user_config_dir = os.path.expanduser("~")
    user_config = user_config_dir + "/.eisen_engine.conf"

    if not os.path.isfile(user_config):
        #os.makedirs(user_config_dir, exist_ok=True)
        shutil.copyfile(".eisen_engine.conf", user_config)

    config = configparser.ConfigParser()
    config.read(user_config)
    return config