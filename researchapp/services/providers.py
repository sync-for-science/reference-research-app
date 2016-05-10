""" Providers Service
"""
from researchapp.models import DBSession
from researchapp.models.providers import Provider


def provider_service(which='db'):
    """ factory method """
    if which == 'file':
        return FileService()
    if which == 'db':
        return DbService()


class DbService(object):
    """ Database backed ParticipantService
    """

    def __init__(self):
        """ init """

    def _query(self, **kwargs):
        """ Builds a Query to be used downstream. """

        return DBSession.query(Provider).filter_by(**kwargs)

    def filter_providers(self, **kwargs):
        """ Return all the matching providers """

        return self._query(**kwargs).all()

    def find_provider(self, **kwargs):
        """ Find a single provider """

        return self._query(**kwargs).one()


class FileService(object):
    """ Local file backed Providers Service
    """

    def __init__(self):
        """ File backed provider service """
        self.providers = self._load_providers()

    def filter_providers(self, **kwargs):
        """ Return all the matching providers """
        providers = self.providers

        if 'name' in kwargs:
            providers = [provider for provider in providers
                         if provider.name == kwargs['name']]

        return providers

    def find_provider(self, **kwargs):
        """ Find a single provider """
        providers = self.filter_providers(**kwargs)

        return next(iter(providers))

    def _load_providers(self):
        import json

        try:
            with open('providers.json') as handle:
                providers = [Provider(**provider) for provider
                             in json.load(handle)]
                return providers
        except FileNotFoundError:
            return []
