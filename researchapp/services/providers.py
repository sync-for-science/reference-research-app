""" Providers Service
"""
from researchapp.models import DBSession
from researchapp.models.providers import Practitioner


def provider_service(which='db'):
    """ factory method """
    if which == 'db':
        return DbService()


class DbService(object):
    """ Database backed ProviderService
    """

    def __init__(self):
        pass

    def _query(self, **kwargs):
        """ Builds a Query to be used downstream.
        """
        return DBSession.query(Practitioner).filter_by(**kwargs)

    def filter_providers(self, **kwargs):
        """ Return all the matching practitioners.
        """
        return self._query(**kwargs).all()

    def find_provider(self, **kwargs):
        """ Find a single practitioner.
        """
        return self._query(**kwargs).one()
