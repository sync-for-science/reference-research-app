""" Log stuff to ElasticSearch so we can look at it later. """
import datetime
import json
import os
import requests


def log(response, *args, **kwargs):  # pylint: disable=unused-argument
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


def _clean(loggable):
    """ Limits requests and responses to just a few fields we care about and
    makes sure that they're json-serializable.

    Fields:
        - body
        - headers
        - method
        - url
    """
    valid = ['body', 'headers', 'method', 'url']
    data = {k: v for k, v in vars(loggable).items() if k in valid}

    data['headers'] = dict(data['headers'])

    if hasattr(loggable, 'text'):
        data['body'] = loggable.text

    return data
