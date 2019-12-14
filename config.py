import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SQLALCHEMY_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or f'postgresql://'
        f'{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@'
        f'{os.environ.get("DB_HOST")}/{os.environ.get("DB_NAME")}'
    )
