from sqlalchemy import *
from bin import db
import time

def start_engine():
    engine = create_engine('mysql://root:password@192.168.33.15:3306/eisen',
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

class task_result(db.Model):
    __tablename__ = "task_result"

    task_id = db.Column(db.String(10), primary_key=True)
    task_result = db.Column(db.String(200), nullable=False)
    target_host = db.Column(db.String(20), nullable=False)

    def __init__(self, task_id, task_result, target_host):
        self.task_id = task_id
        self.task_result = task_result
        self.target_host = target_host

    def __repr__(self):
        return '{}, {}'.format(self.task_id, self.task_result, self.target_host)

class package_result(db.Model):
    __tablename__ = "package_result"

    result_string = db.Column(db.String(256), primary_key=True)
    packageName = db.Column(db.String(256), nullable=False)
    packageVersion = db.Column(db.String(256), nullable=False)
    targetOS = db.Column(db.String(256), nullable=False)
    targetHost = db.Column(db.String(256), nullable=False)
    task_id = db.Column(db.String(256), nullable=False)
    result_short = db.Column(db.String(256), nullable=False)


    def __init__(self, result_string, packageName, packageVersion, targetOS,
                 targetHost, task_id, packageAction, result_short):
        self.result_string = result_string
        self.packageName = packageName
        self.packageVersion = packageVersion
        self.targetOS = targetOS
        self.targetHost = targetHost
        self.task_id = task_id
        self.packageAction = packageAction
        self.result_short = result_short

    def __repr__(self):
        return '{}, {}'.format(self.result_short, self.packageName,
                               self.packageVersion, self.targetOS, self.targetHost,
                               self.task_id, self.packageAction, self.result_short)