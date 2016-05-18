# pylint: disable=missing-docstring,redefined-outer-name
import json

from sqlalchemy import create_engine, orm
import httpretty
import pytest

from researchapp.models import Base
from researchapp.services import fhir


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = orm.sessionmaker(bind=engine)  # pylint: disable=invalid-name

    return Session()


@pytest.fixture
def success_code_to_token(request):
    """ Mocks a successful authorization code exchange. """

    def teardown():
        httpretty.disable()
    request.addfinalizer(teardown)
    httpretty.enable()

    response = {
        'rest': [{
            'security': {
                'extension': [{
                    'url': fhir.OAUTH_URIS_DEFINITION,
                    'extension': [
                        {
                            'url': 'token',
                            'valueUri': 'http://example.com/oauth/token',
                        },
                        {
                            'url': 'authorize',
                            'valueUri': 'http://example.com/oauth/authorize',
                        },
                    ],
                }],
            },
        }],
    }
    httpretty.register_uri(httpretty.GET,
                           'http://example.com/fhir/metadata',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')

    response = {
        'scope': 'patient/*.read',
        'access_token': 'ACCESS TOKEN',
        'token_type': 'token',
        'client_id': 'CLIENT ID',
        'patient': 1,
        'refresh_token': 'REFRESH TOKEN',
    }
    httpretty.register_uri(httpretty.POST,
                           'http://example.com/oauth/token',
                           body=json.dumps(response),
                           status=200,
                           content_type='application/json')
