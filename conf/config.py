import os


class Config(object):
    DEBUG = False
    HOST = os.environ.get("HOST")
    PORT = os.environ.get("PORT")
    SECRET_KEY = os.environ.get("key")
    MONGO_HOST = 'localhost'
    MONGO_PORT = '27017'
    MONGO_DBNAME = 'quotes'


# END CONFIG

class LocalConfig(Config):
    DEBUG = True
    PORT = os.environ.get('PORT')


# END LOCALCONFIG


class DevelopConfig(Config):
    HOST = os.environ.get('HOST')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    PORT = os.environ.get('PORT')
    # END DEVELOP
