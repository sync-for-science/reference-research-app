""" Log stuff to ElasticSearch so we can look at it later. """
import datetime
import json
import requests


ES_URL = 'https://search-s4s-logs-xsjsafiwd7vkpiucmjqmdjkp7y.us-west-2.es.amazonaws.com/' \
        + 'reference-research-app/log/'


def log(response):
    """ Log the response from a FHIR query.

    Parameters
    ----------
    response : requests.models.Response
    """
    payload = {
        'request': _clean(response.request),
        'response': _clean(response),
        'now': datetime.datetime.now().isoformat(),
    }

    requests.post(ES_URL, data=json.dumps(payload))


def _clean(data):
    """ Limits requests and responses to just a few fields we care about and
    makes sure that they're json-serializable.

    Fields:
        - body
        - headers
        - method
        - url
    """
    valid = ['body', 'headers', 'method', 'url']
    data = {k: v for k, v in vars(data).items() if k in valid}

    data['headers'] = dict(data['headers'])

    return data
