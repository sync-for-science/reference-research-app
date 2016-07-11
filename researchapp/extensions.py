""" Flask and other extensions instantiated here.

To avoid circular imports with views and create_app(), extensions are
instantiated here. They will be initialized (calling init_app()) in
application.py.
"""
from flask_sqlalchemy import SQLAlchemy
from injector import singleton


db = SQLAlchemy()  # pylint: disable=invalid-name


def configure(binder):
    """ Add any flask extensions to the injector.
    """
    binder.bind(SQLAlchemy, db, scope=singleton)
