""" FHIR service """
import requests
from researchapp.services.logging import log
from researchapp.services import oauth


OAUTH_URIS_DEFINITION = 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris'


def get_oauth_uris(provider):
    """ Conformance statement should define a set of oauth uris.

    See: http://fhir-docs.smarthealthit.org/argonaut-dev/specification/#5

    Params
    ------
    provider : dict
        fhir_url : string

    Return
    ------
    dict :
        authorize : string
        token : string
    """
    url = '{url}/metadata'.format(url=provider['fhir_url'])
    headers = {
        'Accept': 'application/json+fhir',
    }
    response = requests.get(url, headers=headers)
    conformance = response.json()

    rest = [rest for rest in conformance['rest']][0]
    extension = [ext for ext in rest['security']['extension']
                 if ext['url'] == OAUTH_URIS_DEFINITION][0]

    return {ext['url']: ext['valueUri'] for ext in extension['extension']}


def get_patient(participant, provider):
    """ Gets a Patient resource """
    token = participant.authorization().refresh_token
    auth = oauth.refresh(token, provider)

    url = '{url}/Patient/{patient}'.format(url=provider['fhir_url'],
                                           patient=auth['patient'])
    authorization = '{token_type} {access_token}'.format(**auth)
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)
    log(response)

    return response.json()
