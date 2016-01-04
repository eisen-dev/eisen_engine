from celery import Celery

# global variable used for make function async
celery_work = Celery(__name__, broker='amqp://guest@localhost//', backend='amqp')
