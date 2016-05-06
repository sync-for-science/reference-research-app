""" FHIR service """
import requests
from researchapp.services.logging import log


FHIR_URL = 'http://52.39.26.206:9000/api/fhir'


def get_patient(token):
    """ gets a patient """
    url = '{url}/Patient/{patient}'.format(url=FHIR_URL,
                                           patient=token['patient'])
    authorization = '{token_type} {access_token}'.format(**token)
    headers = {
        'Authorization': authorization,
        'Accept': 'application/json',
    }

    response = requests.get(url, headers=headers)
    log(response)

    return response.json()
