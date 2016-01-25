from celery import Celery
from flask.ext.sqlalchemy import SQLAlchemy

# global variable used for make function async
celery_work = Celery(__name__, broker='amqp://guest@localhost//', backend='amqp')

db = SQLAlchemy()

