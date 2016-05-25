class Config(object):
    DEBUG = False
    # HOST = os.environ.get("HOST")
    SECRET_KEY = '^*d^032DZQX48221d3ZA'
    # HOST = '127.0.0.1'
    # PORT = 5000
    # MONGO_HOST = 'localhost'
    # MONGO_PORT = '27017'
    # MONGO_DBNAME = 'enera'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_DB = 'enera'
    # MONGODB_USERNAME = ''
    # MONGODB_PASSWORD = ''


# END CONFIG

class LocalConfig(Config):
    DEBUG = True
    PORT = 5000
    MONGODB_DB = 'enera'
    MONGODB_HOST = '127.0.0.1'
    MONGODB_PORT = 27017
    MONGODB_USERNAME = 'enera'
    MONGODB_PASSWORD = 'enera'
    # MONGO_HOST = 'ds056998.mongolab.com'
    # MONGO_PORT = 56998
    # MONGO_DBNAME = 'enera'
    # MONGO_USERNAME = 'enera'
    # MONGO_PASSWORD = 'enera'


# END LOCALCONFIG


class DevelopConfig(Config):
    PORT = 5000
    MONGO_HOST = 'ds056998.mongolab.com'
    MONGO_PORT = 56998
    MONGO_DBNAME = 'enera'
    MONGO_USERNAME = 'enera'
    MONGO_PASSWORD = 'enera'
    # HOST = '0.0.0.0'
    # MONGO_HOST = 'http://dev-hackergarage.ppnvvkijpm.us-west-1.elasticbeanstalk.com/'
    # HOST = os.environ.get("HOST")
    # MONGO_HOST = os.environ.get("MONGO_HOST")
    # PORT = os.environ.get("PORT")
    # END DEVELOP
