""" Main """
from pyramid_beaker import session_factory_from_settings
from pyramid.config import Configurator
from pyramid_jinja2 import renderer_factory
from sqlalchemy import engine_from_config

from researchapp.models import initialize_sql


def main(global_config, **settings):  # pylint: disable=unused-argument
    """ This function returns a WSGI application.

    It is usually called by the PasteDeploy framework during
    ``paster serve`` or ``pserve``.
    """
    # SQLAlchemy engine config for main DB
    # Any setting that begins with 'sqlalchemy.' will be picked up
    db_engine = engine_from_config(settings, 'sqlalchemy.')
    # Binding engine to the model
    initialize_sql(db_engine)

    config = Configurator(settings=settings,
                          root_factory='researchapp.models.Root')

    session_factory = session_factory_from_settings(settings)
    config.set_session_factory(session_factory)

    # The views/routes are added here
    config.add_static_view('static', 'static')

    config.add_route('home', '/')
    config.add_route('share_my_data', '/share-my-data')
    config.add_route('consent', '/consent')
    config.add_route('connected', '/connected')
    config.add_route('authorized', '/authorized')
    config.scan()

    return config.make_wsgi_app()
