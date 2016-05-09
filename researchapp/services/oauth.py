""" Oauth """
import requests


def code_to_token(code, provider):
    """ hi """
    from researchapp.services import fhir
    token_url = fhir.get_oauth_uris(provider)['token']
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': 'app-demo',
        'code': code,
    }
    client_auth = requests.auth.HTTPBasicAuth('app-demo',
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
        'client_id': 'app-demo',
    }
    client_auth = requests.auth.HTTPBasicAuth('app-demo',
                                              'demo-secret-s4s')

    response = requests.post(token_url,
                             auth=client_auth,
                             data=post_data)

    return response.json()
