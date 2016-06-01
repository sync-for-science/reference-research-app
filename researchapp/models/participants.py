""" Participants

Participants are the prototypical "users" of this application.
"""
from sqlalchemy import (
    Table,
    ForeignKey,
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from . import Base


PARTICIPANT_AUTHORIZATION = Table(
    'participant_authorization',
    Base.metadata,
    Column('participant_id', ForeignKey('participant.id'), primary_key=True),
    Column('authorization_id', ForeignKey('authorization.id'), primary_key=True)
)


class Participant(Base):
    """ Participant """
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)

    # one to many Participant->Authorization
    authorizations = relationship('Authorization',
                                  secondary=PARTICIPANT_AUTHORIZATION)

    def authorization(self, practitioner):
        """ We want the most recent authorization.
        """
        authorizations = [authz for authz in self.authorizations
                          if authz.practitioner == practitioner]
        try:
            return authorizations[-1]
        except IndexError:
            return None


class Authorization(Base):
    """ Authorization """
    __tablename__ = 'authorization'
    id = Column(Integer, primary_key=True)
    scope = Column(String)
    access_token = Column(String)
    token_type = Column(String)
    client_id = Column(String)
    patient = Column(String)
    refresh_token = Column(String)

    # many to one Authorization -> Practitioner
    practitioner_id = Column(Integer, ForeignKey('practitioner.id'))
    practitioner = relationship('Practitioner')

    def update(self, token):
        self.access_token = token.get('access_token', self.access_token)
        self.refresh_token = token.get('refresh_token', self.refresh_token)
