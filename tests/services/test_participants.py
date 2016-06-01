# pylint: disable=missing-docstring
from sqlalchemy import orm
import pytest

from researchapp.models.providers import Practitioner, Organization, Api
from researchapp.models import Participant
from researchapp.services import participants


def test_get_participant(session):
    service = participants.DbService(session)

    participant = Participant(id=1)
    session.add(participant)

    found = service.get_participant(1)
    assert found.id == 1

    with pytest.raises(orm.exc.NoResultFound):
        service.get_participant(12345)


@pytest.mark.usefixtures('success_code_to_token')
def test_store_authorization(session):
    service = participants.DbService(session)

    participant = Participant(id=1)
    session.add(participant)

    grant = {
        'code': '12345',
    }
    api = Api(url='http://example.com/fhir')
    organization = Organization(api=api)
    practitioner = Practitioner(organization=organization)

    assert participant.authorization() is None

    service.store_authorization(grant, practitioner)

    assert participant.authorization() is not None
