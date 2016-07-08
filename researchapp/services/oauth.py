""" Oauth """
import os

import requests


def code_to_token(code, practitioner):
    """ hi """
    from researchapp.services import fhir
    token_url = fhir.get_oauth_uris(practitioner)['token']
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': practitioner.client_id,
        'redirect_uri': redirect_uri(),
        'code': code,
    }
    client_auth = requests.auth.HTTPBasicAuth(practitioner.client_id,
                                              practitioner.client_secret)
    response = requests.post(token_url,
                             auth=client_auth,
                             data=post_data)

    return response.json()


def refresh(token, practitioner):
    """ hi """
    from researchapp.services import fhir
    token_url = fhir.get_oauth_uris(practitioner)['token']
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': token,
        'client_id': practitioner.client_id,
    }
    client_auth = requests.auth.HTTPBasicAuth(practitioner.client_id,
                                              practitioner.client_secret)

    response = requests.post(token_url,
                             auth=client_auth,
                             data=post_data)

    try:
        return response.json()
    except:
        return {'error': 'invalid json'}


def redirect_uri():
    """ Determine the correct redirect_uri based on ENV variables.
    """
    host = os.getenv('LETSENCRYPT_HOST')
    if host is not None:
        return 'https://' + host + '/authorized'
    else:
        return 'http://' + os.getenv('VIRTUAL_HOST', 'localhost:9003') + '/authorized'
