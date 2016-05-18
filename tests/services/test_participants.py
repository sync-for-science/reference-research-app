# pylint: disable=missing-docstring
from sqlalchemy import orm
import pytest

from researchapp.models import Participant, Provider
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
    provider = Provider(fhir_url='http://example.com/fhir')

    assert participant.authorization() is None

    service.store_authorization(grant, provider)

    assert participant.authorization() is not None
