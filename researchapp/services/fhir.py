""" FHIR service """
import requests
from researchapp.services.logging import log
from researchapp.services import oauth


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
