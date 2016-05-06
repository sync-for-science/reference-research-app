""" I'm a cli script """
import os
import sys
import transaction

from sqlalchemy import engine_from_config

from pyramid.paster import get_appsettings, setup_logging


from .models import (
    DBSession,
    Base,
    Participant,
)


def usage(argv):
    """ print usage hint """
    cmd = os.path.basename(argv[0])
    print('usage: {cmd} <config_uri>\n'
          '(example: "{cmd} development.ini")'.format(cmd=cmd))
    sys.exit(1)


def main(argv=sys.argv):  # pylint: disable=dangerous-default-value
    """ build all our tables """
    if len(argv) != 2:
        usage(argv)
    config_uri = argv[1]
    setup_logging(config_uri)
    settings = get_appsettings(config_uri, name='ResearchApp')
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

    with transaction.manager:
        model = Participant()
        DBSession.add(model)
