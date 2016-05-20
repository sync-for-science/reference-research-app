""" Oauth """
import os

import requests


CLIENT_ID = 'research-app'


def code_to_token(code, provider):
    """ hi """
    from researchapp.services import fhir
    token_url = fhir.get_oauth_uris(provider)['token']
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'code': code,
    }
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID,
                                              'demo-secret-s4s')
    response = requests.post(token_url,
                             auth=client_auth,
                             data=post_data)

    return response.json()


def refresh(token, provider):
    """ hi """
    from researchapp.services import fhir
    token_url = fhir.get_oauth_uris(provider)['token']
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': token,
        'client_id': CLIENT_ID,
    }
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID,
                                              'demo-secret-s4s')

    response = requests.post(token_url,
                             auth=client_auth,
                             data=post_data)

    return response.json()


def redirect_uri():
    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        return 'https://' + host + '/authorized'
    else:
        return 'http://' + os.getenv('VIRTUAL_HOST') + '/authorized'
