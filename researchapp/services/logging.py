""" Log stuff to ElasticSearch so we can look at it later. """
import datetime
import json
import os

import grequests


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

    # Use the asynchronous grequests library because we don't need a response.
    req = grequests.post(es_url, data=json.dumps(payload))
    grequests.send(req)


def _clean(loggable):
    """ Limits requests and responses to just a few fields we care about and
    makes sure that they're json-serializable.

    Fields:
        - body
        - headers
        - json
        - method
        - url
    """
    valid = ['body', 'headers', 'method', 'url']
    data = {k: v for k, v in vars(loggable).items() if k in valid}

    data['headers'] = dict(data['headers'])

    if hasattr(loggable, 'text'):
        data['body'] = loggable.text

    try:
        data['json'] = loggable.json()
    except:  # pylint: disable=bare-except
        pass

    return data
