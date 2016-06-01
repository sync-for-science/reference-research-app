""" FHIR service """
import requests
from researchapp.services.logging import log
from researchapp.services import oauth


OAUTH_URIS_DEFINITION = 'http://fhir-registry.smarthealthit.org/StructureDefinition/oauth-uris'


def get_oauth_uris(practitioner):
    """ Conformance statement should define a set of oauth uris.

    See: http://fhir-docs.smarthealthit.org/argonaut-dev/specification/#5

    Params
    ------
    practitioner : researchapp.models.providers.Practitioner

    Return
    ------
    dict :
        authorize : string
        token : string
    """
    url = '{url}metadata'.format(url=practitioner.fhir_url)
    headers = {
        'Accept': 'application/json+fhir',
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200, \
        'Non-200 status code {0} for {url}'.format(response.status_code,
                                                   url=url)
    conformance = response.json()

    rest = [rest for rest in conformance['rest']][0]
    extension = [ext for ext in rest['security']['extension']
                 if ext['url'] == OAUTH_URIS_DEFINITION][0]

    return {ext['url']: ext['valueUri'] for ext in extension['extension']}


def get_patient(participant, provider):
    """ Gets a Patient resource """
    token = participant.authorization().refresh_token
    auth = oauth.refresh(token, provider)

    url = '{url}Patient/{patient}'.format(url=provider.fhir_url,
                                           patient=auth['patient'])
    authorization = '{token_type} {access_token}'.format(**auth)
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)
    log(response)

    return response.json()


def query(participant, provider, resource):
    """ Does a query.

    TODO: needs to support pagination.
    """
    token = participant.authorization(provider).refresh_token
    auth = oauth.refresh(token, provider)

    participant.authorization(provider).update(auth)

    resource = resource.format(patientId=auth['patient'])
    url = '{url}{resource}'.format(url=provider.fhir_url,
                                    resource=resource)

    authorization = '{token_type} {access_token}'.format(**auth)
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)
    log(response)

    assert response.status_code == 200, \
        'Non-200 status code {0}'.format(response.status_code)

    return response.json()
