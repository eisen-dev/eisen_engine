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
import config_action

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    config_action.write()
    config = config_action.read()

    SECRET_KEY = os.environ.get(config['REST']['SECRET_KEY']) or 'hard to guess string'
    SSL_DISABLE = bool(config['SSL']['SSL_DISABLE'])
    SQLALCHEMY_COMMIT_ON_TEARDOWN = config['SQLALCHEMY']['SQLALCHEMY_COMMIT_ON_TEARDOWN']
    SQLALCHEMY_RECORD_QUERIES = bool(config['SQLALCHEMY']['SQLALCHEMY_RECORD_QUERIES'])
    CELERY_BROKER_URL = config['CELERY']['CELERY_BROKER_URL']
    CELERY_RESULT_BACKEND = config['CELERY']['CELERY_RESULT_BACKEND']
    SQLALCHEMY_DATABASE_URI = config['SQLALCHEMY']['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(config['SQLALCHEMY']['SQLALCHEMY_TRACK_MODIFICATIONS'])

    @staticmethod
    def init_app(app):
        pass