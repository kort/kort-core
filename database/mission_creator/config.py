# config.py


import os


class BaseConfig(object):

    # check which environment it runs on
    if os.getenv('SECRET_KEY'):
        SECRET_KEY = os.environ['SECRET_KEY']
        DEBUG = os.environ['DEBUG']
        DB_NAME = os.environ['DB_NAME']
        DB_USER = os.environ['DB_USER']
        DB_PASS = os.environ['DB_PASS']
        DB_SERVICE = 'localhost'
        DB_PORT = os.environ['DB_PORT']
        SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
        )

    else:
        SECRET_KEY = 'mySecretKey'
        DEBUG = True
        DB_NAME = 'osm_bugs'
        DB_PASSWORD = 'postgres'
        DB_USER = 'osm'
        DB_SERVICE = 'localhost'
        DB_PORT = 5432
        SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASSWORD, DB_SERVICE, DB_PORT, DB_NAME
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = True

