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
from bin import db
from config import Config
import time

def start_engine():
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,
                       echo=True)
    metadata = MetaData(bind=engine)
    return engine, metadata

def sendTaskToDb(engine, metadata, connection, task, target_host):
    while task.ready() is False:
        time.sleep(1)
    tasks_result = str(task.get())
    repository_package = Table('task_result', metadata, autoload=True,
                    autoload_with=engine)
    stmt = repository_package.insert()
    connection.execute(
        stmt,
        task_id=task,
        task_result=tasks_result,
        target_host=target_host,
    ).execution_options(autocommit=True)
    connection.close()