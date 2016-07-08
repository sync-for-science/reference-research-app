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

from researchapp.extensions import db


PARTICIPANT_AUTHORIZATION = db.Table(
    'participant_authorization',
    Column('participant_id', ForeignKey('participant.id'), primary_key=True),
    Column('authorization_id', ForeignKey('authorization.id'), primary_key=True)
)


class Participant(db.Model):
    """ Participant """
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)

    # one to many Participant->Authorization
    authorizations = relationship('Authorization',
                                  secondary=PARTICIPANT_AUTHORIZATION)

    @property
    def practitioners(self):
        practitioners = set()
        for authz in self.authorizations:
            practitioners.add(authz.practitioner)

        return practitioners


    def authorization(self, practitioner):
        """ We want the most recent authorization.
        """
        authorizations = [authz for authz in self.authorizations
                          if authz.practitioner == practitioner]
        try:
            return authorizations[-1]
        except IndexError:
            return None


class Authorization(db.Model):
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
