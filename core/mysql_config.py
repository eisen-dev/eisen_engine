from sqlalchemy import *
from bin import db
import time

def start_engine():
    engine = create_engine('mysql://root:password@192.168.33.15:3306/eisen?charset=utf8',
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