""" models """
from pyramid.security import Allow, Everyone

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

class Root(object):
    def __init__(self, request):
        pass

def initialize_sql(engine):
    DBSession.configure(bind=engine)

from .participants import Participant
from .providers import Practitioner
