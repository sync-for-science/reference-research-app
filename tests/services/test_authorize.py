# pylint: disable=missing-docstring,redefined-outer-name
from fhirclient import client
import pytest

from researchapp.models import participants, providers
from researchapp.services import authorize


OAUTH_CLIENT_SCOPE = 'patient/*.read'
ORGANIZATION_ID = 'org-corp'
ORGANIZATION_NAME = 'Org Corp.'
ORGANIZATION_URL = 'http://example.com/fhir'
PRACTITIONER_NAME = 'Dr. Test'


@pytest.fixture
def a_participant(session):
    participant = participants.Participant(id=participants.THE_ONLY_PARTICIPANT_ID)

    session.add(participant)
    session.commit()

    return participant


@pytest.fixture
def a_practitioner(session):
    client = providers.OAuthClient(scope=OAUTH_CLIENT_SCOPE)
    organization = providers.Organization(id=ORGANIZATION_ID,
                                          name=ORGANIZATION_NAME,
                                          url=ORGANIZATION_URL,
                                          oauth_client=client)
    practitioner = providers.Practitioner(name=PRACTITIONER_NAME,
                                          organization=organization)

    session.add(practitioner)
    session.commit()

    return practitioner


@pytest.mark.usefixtures('enable_httpretty')
@pytest.mark.parametrize('paths', [['test_metadata_valid.json']])
@pytest.mark.usefixtures('mock_http')
def test_display_consent(db, a_practitioner):  # pylint: disable=invalid-name
    service = authorize.AuthorizeService(db)
    redirect_uri = 'http://example.com/authorized'
    session = {}

    view_data = service.display_consent(PRACTITIONER_NAME,
                                        redirect_uri,
                                        session)

    assert view_data['authorize_url']
    assert session['practitioner_id'] == a_practitioner.id


@pytest.mark.usefixtures('enable_httpretty')
@pytest.mark.parametrize('paths', [[
    'test_metadata_valid.json',
    'test_oauth_token.json',
]])
@pytest.mark.usefixtures('mock_http')
@pytest.mark.usefixtures('a_participant')
def test_register_authorization(db, a_practitioner):  # pylint: disable=invalid-name
    service = authorize.AuthorizeService(db)
    settings = {
        'app_id': 'example-app',
        'api_base': ORGANIZATION_URL,
    }
    fhir = client.FHIRClient(settings=settings)
    fhir.authorize_url  # pylint: disable=pointless-statement

    session = {
        'practitioner_id': a_practitioner.id,
        'fhirclient': fhir.state,
    }
    callback_url = 'http://example.com/authorized?code=123&state={0}'.\
        format(fhir.state['server']['auth']['auth_state'])

    service.register_authorization(callback_url, session)
