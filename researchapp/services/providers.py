""" Providers Service
"""
from flask_sqlalchemy import SQLAlchemy
from injector import inject

from researchapp.models.providers import Practitioner


class ProviderService(object):
    """ The service.
    """
    @inject(db=SQLAlchemy)
    def __init__(self, db):
        self._db = db

    def _query(self, **kwargs):
        """ Builds a Query to be used downstream.
        """
        return self._db.session.query(Practitioner).filter_by(**kwargs)

    def filter_providers(self, **kwargs):
        """ Return all the matching practitioners.
        """
        return self._query(**kwargs).all()

    def find_provider(self, **kwargs):
        """ Find a single practitioner.
        """
        return self._query(**kwargs).one()


def configure(binder):
    """ Configure this module for the Injector.
    """
    binder.bind(ProviderService)
