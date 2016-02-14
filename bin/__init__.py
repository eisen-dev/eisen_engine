from celery import Celery
from flask.ext.sqlalchemy import SQLAlchemy
from config import Config

# global variable used for make function async
celery_work = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

db = SQLAlchemy()

