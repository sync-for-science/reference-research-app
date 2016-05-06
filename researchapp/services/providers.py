""" Providers Service
"""


def provider_service(which='file'):
    """ factory method """
    if which == 'file':
        return FileService()


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
                         if provider['name'] == kwargs['name']]

        return providers

    def find_provider(self, **kwargs):
        """ Find a single provider """
        providers = self.filter_providers(**kwargs)

        return next(iter(providers))

    def oauth_for_provider(self, provider):  # pylint: disable=unused-argument
        """ Returns an OAuth config blob for a provider. """

        return {
            'client_id': 'app-demo',
            'url': 'http://52.39.26.206:9000/api/oauth/',
        }

    def _load_providers(self):
        import json

        try:
            with open('providers.json') as handle:
                return json.load(handle)
        except FileNotFoundError:
            return []
