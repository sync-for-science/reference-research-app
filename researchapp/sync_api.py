''' Library for interfacing with the "synchronizer".
'''
import requests


class SyncExtension(object):
    ''' Flask extension for interacting with the Synchronizer API.
    '''
    def __init__(self, app=None):
        self.session = None
        self.host = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        ''' Init the extension.
        '''
        self.session = requests.Session()
        self.host = app.config['SYNCHRONIZER_HOST']

    def list_providers(self):
        ''' List available providers.
        '''
        resp = self.session.get(self.host + '/providers')
        return resp.json()

    def create_participant(self):
        ''' Create a new participant.
        '''
        resp = self.session.post(self.host + '/participants')
        return resp.json()

    def create_authorization(self, participant_id, redirect_uri):
        ''' Store an authorization.
        '''
        path = '/participants/{}/authorizations'.format(participant_id)
        params = {
            'redirect_uri': redirect_uri,
        }
        resp = self.session.post(self.host + path, data=params)

        assert resp.status_code == 200, resp.json().get('message')

        return resp.json()

    def list_authorizations(self, participant_id):
        ''' Get all the authorizations for a Participant.
        '''
        path = '/participants/{}/authorizations'.format(participant_id)
        resp = self.session.get(self.host + path)
        return resp.json()

    def list_everything(self, participant_id, provider_id):
        ''' Get all the Resources for a Participant for a given provider.
        '''
        path = '/particpants/{}/authorizations/{}/$everything'.format(participant_id, provider_id)
        resp = self.session.get(self.host + path)
        return resp.json()

    def get_provider_launch_url(self, provider_id, participant_id):
        ''' Get the url to start the OAuth handshake.
        '''
        path = '/providers/{}/launch/{}'.format(provider_id, participant_id)
        resp = self.session.post(self.host + path, allow_redirects=False)

        return resp.headers['Location']
