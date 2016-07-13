# pylint: disable=missing-docstring
import pytest

from researchapp.models import participants


@pytest.mark.usefixtures('db')
def test_create_participant():
    participant = participants.Participant()

    assert participant
