# pylint: disable=missing-docstring,redefined-outer-name,unused-argument
import os

from flask import Flask
import frontmatter
import pytest
import httpretty

from researchapp.extensions import db as _db
from researchapp.models import (  # pylint: disable=unused-import
    participants,
    providers,
    resources,
)


@pytest.fixture
def enable_httpretty(request):
    """ Enables httpretty request intercepting for a single test.
    """
    httpretty.enable()
    request.addfinalizer(httpretty.disable)


@pytest.fixture
def mock_http(request, paths):
    """ Defines a conformance statement with token and authorize uris.
    """
    for path in paths:
        path = os.path.join('./tests/mocks/', path)
        mock = frontmatter.load(path)
        httpretty.register_uri(body=mock.content, **mock)


@pytest.fixture(scope='function')
def app(request):
    """ Flask application.
    """
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    # Establish an application context
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)

    return app


@pytest.fixture(scope='function')
def db(app, request):  # pylint: disable=invalid-name
    """ Test database.
    """

    def teardown():
        _db.drop_all()

    _db.init_app(app)
    _db.create_all()

    request.addfinalizer(teardown)

    return _db


@pytest.fixture(scope='function')
def session(db, request):  # pylint: disable=invalid-name
    """ Creates a new database session for a test.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
