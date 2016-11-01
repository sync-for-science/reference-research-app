# pylint: disable=missing-docstring
from researchapp import application


def test_create_app():
    assert application.create_app()
