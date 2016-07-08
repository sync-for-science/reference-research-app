# pylint: disable=missing-docstring
class Config(object):
    """ Default Flask configuration inherited by all environments.
    Use this for development environments.
    """
    DEBUG = True
    TESTING = False
    SECRET_KEY = '19ab3891bc320f9a197b671437125728'

    DB_MODELS_IMPORTS = ('participants', 'providers', 'resources',)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Testing(Config):
    TESTING = True


class Production(Config):
    DEBUG = False
    SECRET_KEY = None  # To be overwritten by a YAML file.
