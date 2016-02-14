import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    CELERY_BROKER_URL = 'amqp://guest@localhost//'
    CELERY_RESULT_BACKEND = 'amqp'
    SQLALCHEMY_DATABASE_URI="mysql://root:password@192.168.33.15:3306/eisen"
    SQLALCHEMY_TRACK_MODIFICATIONS=False

    @staticmethod
    def init_app(app):
        pass