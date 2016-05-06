""" Oauth """
import requests


TOKEN_URL = 'http://52.39.26.206:9000/api/oauth/token'


def code_to_token(code):
    """ hi """
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': 'app-demo',
        'code': code,
    }
    client_auth = requests.auth.HTTPBasicAuth('app-demo',
                                              'demo-secret-s4s')
    response = requests.post(TOKEN_URL,
                             auth=client_auth,
                             data=post_data)

    try:
        return response.json()
    except ValueError:
        print(response.text)
        return {}


def refresh(token):
    """ hi """
    post_data = {
        'grant_type': 'refresh_token',
        'refresh_token': token,
        'client_id': 'app-demo',
    }
    client_auth = requests.auth.HTTPBasicAuth('app-demo',
                                              'demo-secret-s4s')

    response = requests.post(TOKEN_URL,
                             auth=client_auth,
                             data=post_data)

    try:
        return response.json()
    except ValueError:
        print(response.text)
        return {}
