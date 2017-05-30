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
        DB_SERVICE = os.environ['DB_SERVICE']
        DB_PORT = os.environ['DB_PORT']
        SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASS, DB_SERVICE, DB_PORT, DB_NAME
        )

        TOKENINFO_HOST = '0.0.0.0'
        TOKENINFO_URL = os.environ['TOKENINFO_URL']

        #OAuth variables
        GOOGLE_ID = os.environ['GOOGLE_ID']
        GOOGLE_SECRET = os.environ['GOOGLE_SECRET']

        OSM_CONSUMER_KEY = os.environ['OSM_CONSUMER_KEY']
        OSM_CONSUMER_SECRET = os.environ['OSM_CONSUMER_SECRET']

    else:
        SECRET_KEY = 'mySecretKey'
        DEBUG = True
        DB_NAME = 'osm_bugs'
        DB_PASSWORD = 'postgres'
        DB_USER = 'egloff'
        DB_SERVICE = 'localhost'
        DB_PORT = 5432
        SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
            DB_USER, DB_PASSWORD, DB_SERVICE, DB_PORT, DB_NAME
        )

        TOKENINFO_HOST = '127.0.0.1'
        TOKENINFO_URL = 'http://localhost:7979/tokeninfo'
        os.environ['TOKENINFO_URL'] = TOKENINFO_URL

        #OAuth variables

        GOOGLE_ID ='643328561815-4mi1d07c09ef23mqnks1on3dj77snd7g.apps.googleusercontent.com'
        GOOGLE_SECRET = 'nFwkqnbUk-IHefg7DdF0W0qy'

        OSM_CONSUMER_KEY = 'Yx5MfCY9PI4LZkO1Jjl2nY1LdGdiXm85e70Pu2cw'
        OSM_CONSUMER_SECRET = 'UQdzXO1tu3ECDiIawSnODRz8BeUGCOkb7SejZtJN'

        # #OAuth variables
        # GOOGLE_ID = os.environ['GOOGLE_ID']
        # GOOGLE_SECRET = os.environ['GOOGLE_SECRET']
        #
        # OSM_CONSUMER_KEY = os.environ['OSM_CONSUMER_KEY']
        # OSM_CONSUMER_SECRET = os.environ['OSM_CONSUMER_SECRET']
        #
        # TOKENINFO_HOST = '0.0.0.0'
        # TOKENINFO_URL = os.environ['TOKENINFO_URL']

    SQLALCHEMY_TRACK_MODIFICATIONS = True

