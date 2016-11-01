''' Library for interfacing with the "synchronizer".
'''
from json.decoder import JSONDecodeError

import requests


class SyncExtension(object):
    def __init__(self, app=None):
        self.session = None
        self.host = None

        if app:
            self.init_app(app)

    def init_app(self, app):
        self.session = requests.Session()
        self.host = app.config['SYNCHRONIZER_HOST']

    def list_providers(self):
        resp = self.session.get(self.host + '/providers')
        return resp.json()

    def create_participant(self):
        resp = self.session.post(self.host + '/participants')
        return resp.json()

    def create_authorization(self, participant_id, provider_id, redirect_uri):
        path = '/participants/{}/authorizations/{}'.format(participant_id, provider_id)
        params = {
            'redirect_uri': redirect_uri,
        }
        resp = self.session.post(self.host + path, data=params)
        return resp.json()

    def list_authorizations(self, participant_id):
        path = '/participants/{}/authorizations'.format(participant_id)
        resp = self.session.get(self.host + path)
        try:
            return resp.json()
        except JSONDecodeError:
            print(self.host)
            print(path)
            raise

    def list_everything(self, participant_id, provider_id):
        path = '/particpants/{}/authorizations/{}/$everything'.format(participant_id, provider_id)
        resp = self.session.get(self.host + path)
        return resp.json()

    def get_provider_launch_url(self, provider_id):
        path = '/providers/{}/launch'.format(provider_id)
        return self.host + path

