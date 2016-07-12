""" Log stuff to ElasticSearch so we can look at it later. """
import datetime
import json
import os
import requests


def log(response):
    """ Log the response from a FHIR query.

    Parameters
    ----------
    response : requests.models.Response
    """
    es_url = os.getenv('ES_URL')

    payload = {
        'request': _clean(response.request),
        'response': _clean(response),
        'now': datetime.datetime.now().isoformat(),
    }

    requests.post(es_url, data=json.dumps(payload))


def _clean(data):
    """ Limits requests and responses to just a few fields we care about and
    makes sure that they're json-serializable.

    Fields:
        - body
        - headers
        - method
        - url
    """
    valid = ['body', '_content', 'headers', 'method', 'url']
    data = {k: v for k, v in vars(data).items() if k in valid}

    data['headers'] = dict(data['headers'])

    if '_content' in data:
        data['body'] = data['_content'].decode('utf-8')
        del data['_content']

    return data
